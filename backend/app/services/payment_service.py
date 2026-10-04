import asyncio
import logging
import uuid
from datetime import datetime
from typing import List, Dict, Any
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.models import Show, Seat, Booking, BookingSeat, Screen, Theater, Movie, User
from app.services.ticket_service import TicketService
from app.redis_client import release_seat_lock, get_seat_lock_info

logger = logging.getLogger("ticketlocal.payment")

class PaymentService:
    @staticmethod
    async def calculate_fees(show_id: int, seat_ids: List[int], db: AsyncSession) -> Dict[str, Any]:
        """
        Calculates fee breakdown:
        Base Seat Prices + 10% Convenience Fee + 18% GST on convenience fee.
        """
        show = await db.get(Show, show_id)
        if not show:
            raise HTTPException(status_code=404, detail="Show not found")

        seats_res = await db.execute(select(Seat).where(Seat.id.in_(seat_ids)))
        seats = seats_res.scalars().all()
        if len(seats) != len(seat_ids):
            raise HTTPException(status_code=400, detail="Some seats are invalid")

        surge = show.surge_multiplier or 1.0
        seat_items = []
        base_amount = 0.0

        for seat in seats:
            price = round(seat.base_price * surge, 2)
            base_amount += price
            seat_items.append({
                "seat_id": seat.id,
                "row": seat.row,
                "number": seat.number,
                "seat_type": seat.seat_type,
                "price": price,
            })

        base_amount = round(base_amount, 2)
        # Convenience fee is 10% of base amount
        convenience_fee = round(base_amount * 0.10, 2)
        # 18% GST on convenience fee
        tax_amount = round(convenience_fee * 0.18, 2)
        total_amount = round(base_amount + convenience_fee + tax_amount, 2)

        return {
            "show_id": show_id,
            "seat_count": len(seats),
            "seat_items": seat_items,
            "base_amount": base_amount,
            "convenience_fee": convenience_fee,
            "convenience_fee_rate": 0.10,
            "tax_amount": tax_amount,
            "tax_rate": 0.18,
            "total_amount": total_amount,
        }

    @staticmethod
    async def process_checkout(
        show_id: int,
        seat_ids: List[int],
        user_id: str,
        customer_name: str,
        customer_email: str,
        customer_phone: str,
        payment_method: str,
        db: AsyncSession,
    ) -> Dict[str, Any]:
        """
        Processes checkout with:
        1. Fee calculation & validation
        2. 2000ms async simulated payment processing delay
        3. Atomic PostgreSQL transaction to insert Booking and BookingSeats (ACID)
        4. Redis lock release
        5. Local QR ticket image generation
        """
        # 1. Fee calculation
        fee_data = await PaymentService.calculate_fees(show_id, seat_ids, db)

        # 2. Verify Redis holds for these seats
        for seat_id in seat_ids:
            lock = await get_seat_lock_info(show_id, seat_id)
            if not lock or (lock.get("user_id") != user_id):
                logger.warning(f"Lock expired or missing for seat {seat_id} during checkout.")
                raise HTTPException(
                    status_code=status.HTTP_423_LOCKED,
                    detail=f"Seat hold has expired or was cleared. Please re-select seat {seat_id}."
                )

        # 3. 2000ms simulated payment processing delay
        await asyncio.sleep(2.0)

        # 4. Atomic PostgreSQL transaction
        show_res = await db.execute(
            select(Show)
            .where(Show.id == show_id)
            .options(
                joinedload(Show.movie),
                joinedload(Show.screen).joinedload(Screen.theater),
            )
        )
        show = show_res.unique().scalar_one_or_none()
        if not show:
            raise HTTPException(status_code=404, detail="Show not found")

        # Check user or create guest user
        user_res = await db.execute(select(User).where(User.email == customer_email))
        user = user_res.scalar_one_or_none()
        if not user:
            user = User(
                email=customer_email,
                full_name=customer_name,
                phone=customer_phone,
                role="guest",
            )
            db.add(user)
            await db.flush()

        booking_ref = f"TL-{datetime.utcnow().strftime('%y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        payment_id = f"PAY-{uuid.uuid4().hex[:12].upper()}"
        ticket_id = str(uuid.uuid4())

        # Create Booking
        booking = Booking(
            booking_ref=booking_ref,
            user_id=user.id,
            show_id=show_id,
            base_amount=fee_data["base_amount"],
            convenience_fee=fee_data["convenience_fee"],
            tax_amount=fee_data["tax_amount"],
            total_amount=fee_data["total_amount"],
            status="CONFIRMED",
            payment_method=payment_method,
            payment_id=payment_id,
            created_at=datetime.utcnow(),
        )
        db.add(booking)
        await db.flush()

        # Seat list representation for QR code & response
        seat_names = []
        for item in fee_data["seat_items"]:
            seat_name = f"{item['row']}{item['number']}"
            seat_names.append(seat_name)
            booking_seat = BookingSeat(
                booking_id=booking.id,
                show_id=show_id,
                seat_id=item["seat_id"],
                price=item["price"],
            )
            db.add(booking_seat)

        # 5. Commit transaction atomically
        try:
            await db.commit()
            await db.refresh(booking)
        except Exception as e:
            await db.rollback()
            logger.error(f"ACID Transaction failed during seat booking commit: {e}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Transaction conflict: One or more seats were already booked in a race condition."
            )

        # 6. Generate local QR code PNG
        qr_url = TicketService.generate_qr_ticket(
            ticket_id=ticket_id,
            booking_ref=booking_ref,
            show_id=show_id,
            movie_title=show.movie.title,
            theater_name=show.screen.theater.name,
            seats=seat_names,
            status="PAID",
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
        booking.ticket_qr_path = qr_url
        await db.commit()

        # 7. Release Redis locks
        for s_id in seat_ids:
            await release_seat_lock(show_id, s_id, user_id)

        return {
            "booking_id": booking.id,
            "booking_ref": booking_ref,
            "status": "CONFIRMED",
            "show_id": show_id,
            "movie_title": show.movie.title,
            "theater_name": show.screen.theater.name,
            "screen_name": show.screen.name,
            "show_date": show.show_date,
            "show_time": show.start_time,
            "format": show.format,
            "seats": seat_names,
            "total_amount": booking.total_amount,
            "ticket_qr_url": qr_url,
            "ticket_qr_path": str(settings.TICKETS_DIR / f"ticket_{booking_ref}.png"),
            "payment_id": payment_id,
            "created_at": booking.created_at.isoformat() + "Z",
        }
