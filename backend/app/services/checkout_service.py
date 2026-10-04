import asyncio
import logging
from typing import List, Dict, Any
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import (
    Show, Screen, Theater, Content, Seat, Booking, BookingSeat,
    BookingStatus, Ticket, PricingRule
)
from app.schemas import PaymentCardInput, CartQuoteResponse
from app.redis_client import (
    check_user_holds, release_seat_locks
)
from app.services.pricing_service import PricingService
from app.services.qr_service import generate_ticket_qr
from app.services.chaos_service import chaos_service

logger = logging.getLogger("ticketlocal.checkout")

# Mock test card failure prefix/number
FAILURE_CARD_NUMBER = "4000000000000002"

class CheckoutService:
    @staticmethod
    async def get_cart_quote(
        show_id: int,
        seat_ids: List[int],
        user_id: str,
        db: AsyncSession,
    ) -> Dict[str, Any]:
        # 1. Fetch Show and Pricing Rules
        show = await db.get(Show, show_id)
        if not show:
            raise HTTPException(status_code=404, detail="Show not found")

        rules_res = await db.execute(select(PricingRule))
        rules = {r.seat_type: r for r in rules_res.scalars().all()}

        # 2. Fetch Seats
        seats_res = await db.execute(select(Seat).where(Seat.id.in_(seat_ids)))
        seats = seats_res.scalars().all()
        if len(seats) != len(seat_ids):
            raise HTTPException(status_code=400, detail="Invalid seat IDs specified")

        # 3. Check Redis holds
        holds_valid, min_ttl = await check_user_holds(show_id, seat_ids, user_id)

        # 4. Compute prices
        breakdowns = []
        subtotal = 0.0
        for s in seats:
            rule = rules.get(s.seat_type)
            mult = rule.multiplier if rule else None
            w_surge = rule.weekend_surge if rule else None
            p_surge = rule.prime_time_surge if rule else None

            p = PricingService.calculate_seat_price(
                base_price=show.base_price,
                seat_type=s.seat_type,
                show_time=show.start_time,
                type_multiplier=mult,
                weekend_surge=w_surge,
                prime_time_surge=p_surge,
            )
            subtotal += p
            breakdowns.append({
                "seat_id": s.id,
                "row_label": s.row_label,
                "seat_number": s.seat_number,
                "seat_type": s.seat_type,
                "price": p,
            })

        subtotal = round(subtotal, 2)
        totals = PricingService.calculate_order_totals(
            subtotal=subtotal,
            force_tax_crash=chaos_service.tax_crash_enabled
        )

        return {
            "show_id": show_id,
            "seats": breakdowns,
            "subtotal": totals["subtotal"],
            "convenience_fee": totals["convenience_fee"],
            "convenience_fee_percentage": totals["convenience_fee_percentage"],
            "tax": totals["tax"],
            "tax_percentage": totals["tax_percentage"],
            "total": totals["total"],
            "holds_valid": holds_valid,
            "min_remaining_ttl": min_ttl,
        }

    @staticmethod
    async def process_checkout(
        show_id: int,
        seat_ids: List[int],
        payment: PaymentCardInput,
        user_id: int,
        db: AsyncSession,
    ) -> Dict[str, Any]:
        chaos_service.increment_checkout_attempt()

        # 1. Fetch Show details with relations
        query = (
            select(Show)
            .where(Show.id == show_id)
            .options(
                joinedload(Show.content),
                joinedload(Show.screen).joinedload(Screen.theater),
            )
        )
        res = await db.execute(query)
        show = res.unique().scalar_one_or_none()
        if not show:
            raise HTTPException(status_code=404, detail="Show not found")

        # 2. Verify all Redis holds belong to user
        holds_valid, _ = await check_user_holds(show_id, seat_ids, str(user_id))
        if not holds_valid:
            chaos_service.increment_checkout_failure()
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Your seat hold has expired or was not found. Please re-select your seats."
            )

        # 3. Simulate payment processing delay (2000 ms async sleep)
        await asyncio.sleep(2.0)

        # Check for simulated test failure card
        if payment.card_number.replace(" ", "") == FAILURE_CARD_NUMBER or payment.card_number.endswith("0002"):
            chaos_service.increment_checkout_failure()
            # On failure: mark as failed and keep seats held until TTL expiry
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Payment declined by mock payment gateway. Insufficient funds or invalid test card."
            )

        # 4. Calculate quotes and totals
        quote = await CheckoutService.get_cart_quote(show_id, seat_ids, str(user_id), db)

        # 5. Open PostgreSQL Transaction to create booking and seats
        try:
            booking = Booking(
                user_id=user_id,
                show_id=show_id,
                status=BookingStatus.PAID,
                subtotal=quote["subtotal"],
                convenience_fee=quote["convenience_fee"],
                tax=quote["tax"],
                total=quote["total"],
            )
            db.add(booking)
            await db.flush()  # populate booking.id

            for item in quote["seats"]:
                bs = BookingSeat(
                    booking_id=booking.id,
                    show_id=show_id,
                    seat_id=item["seat_id"],
                    price=item["price"],
                )
                db.add(bs)

            await db.commit()
            await db.refresh(booking)

        except IntegrityError as ie:
            await db.rollback()
            chaos_service.increment_checkout_failure()
            logger.error(f"Postgres unique constraint double-booking collision prevented on show {show_id}, seats {seat_ids}: {ie}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="One or more selected seats were already booked in another transaction. Double booking prevented."
            )
        except Exception as e:
            await db.rollback()
            chaos_service.increment_checkout_failure()
            logger.error(f"Checkout transaction failed: {e}")
            raise

        # 6. Delete Redis locks
        await release_seat_locks(show_id, seat_ids, str(user_id))

        # 7. Generate QR Ticket PNG asynchronously via threadpool
        seat_labels = [f"{s['row_label']}{s['seat_number']}" for s in quote["seats"]]
        qr_path = await generate_ticket_qr(
            booking_id=booking.id,
            booking_ref=f"TKT-{booking.id:06d}",
            content_title=show.content.title if show.content else "Event",
            theater_name=show.screen.theater.name if show.screen and show.screen.theater else "Cinema",
            show_time=show.start_time.strftime("%d %b %Y, %I:%M %p"),
            seats=seat_labels,
            total_amount=quote["total"],
        )

        ticket = Ticket(
            booking_id=booking.id,
            qr_path=qr_path,
        )
        db.add(ticket)
        await db.commit()
        await db.refresh(ticket)

        chaos_service.increment_checkout_success()

        return {
            "success": True,
            "booking_id": booking.id,
            "status": booking.status,
            "total": booking.total,
            "ticket_id": ticket.id,
            "qr_url": f"/api/tickets/{ticket.id}/qr",
            "message": "Payment successful and ticket confirmed!",
        }
