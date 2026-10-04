import logging
from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import (
    Show, Screen, Theater, Content, Seat, Booking, BookingSeat,
    BookingStatus, PricingRule
)
from app.redis_client import (
    acquire_atomic_seat_locks, release_seat_locks, get_all_locks_for_show
)
from app.services.pricing_service import PricingService
from app.services.chaos_service import chaos_service

logger = logging.getLogger("ticketlocal.seats")

class SeatService:
    @staticmethod
    async def get_seat_matrix(
        show_id: int,
        user_id: Optional[str],
        db: AsyncSession
    ) -> Dict[str, Any]:
        # 1. Fetch Show details
        query = (
            select(Show)
            .where(Show.id == show_id)
            .options(
                joinedload(Show.content),
                joinedload(Show.screen).joinedload(Screen.theater),
            )
        )
        result = await db.execute(query)
        show = result.unique().scalar_one_or_none()
        if not show:
            raise HTTPException(status_code=404, detail="Show not found")

        screen = show.screen

        # 2. Fetch all seats for this screen ordered by row, number
        seats_res = await db.execute(
            select(Seat)
            .where(Seat.screen_id == screen.id)
            .order_by(Seat.row_label, Seat.seat_number)
        )
        all_seats = seats_res.scalars().all()

        # 3. Fetch all confirmed/paid seats from PostgreSQL for this show
        booked_res = await db.execute(
            select(BookingSeat.seat_id)
            .join(Booking, BookingSeat.booking_id == Booking.id)
            .where(
                BookingSeat.show_id == show_id,
                Booking.status == BookingStatus.PAID
            )
        )
        booked_seat_ids = set(booked_res.scalars().all())

        # 4. Fetch active Redis locks for this show
        active_locks = await get_all_locks_for_show(show_id)

        # 5. Fetch pricing rules
        rules_res = await db.execute(select(PricingRule))
        rules = {r.seat_type: r for r in rules_res.scalars().all()}

        is_weekend = PricingService.is_weekend(show.start_time)
        is_prime = PricingService.is_prime_time(show.start_time)

        # 6. Group seats by row
        rows_dict: Dict[str, List[Dict[str, Any]]] = {}
        total_available = 0
        total_held = 0
        total_booked = 0

        for seat in all_seats:
            rule = rules.get(seat.seat_type)
            mult = rule.multiplier if rule else None
            w_surge = rule.weekend_surge if rule else None
            p_surge = rule.prime_time_surge if rule else None

            computed_price = PricingService.calculate_seat_price(
                base_price=show.base_price,
                seat_type=seat.seat_type,
                show_time=show.start_time,
                type_multiplier=mult,
                weekend_surge=w_surge,
                prime_time_surge=p_surge,
            )

            seat_status = "AVAILABLE"
            held_by_me = False
            remaining_ttl = None

            if seat.id in booked_seat_ids:
                seat_status = "BOOKED"
                total_booked += 1
            elif seat.id in active_locks:
                seat_status = "HELD"
                lock_info = active_locks[seat.id]
                held_by_me = bool(user_id and str(lock_info.get("user_id")) == str(user_id))
                remaining_ttl = lock_info.get("remaining_ttl_seconds")
                total_held += 1
            else:
                seat_status = "AVAILABLE"
                total_available += 1

            seat_data = {
                "id": seat.id,
                "screen_id": seat.screen_id,
                "row_label": seat.row_label,
                "seat_number": seat.seat_number,
                "seat_type": seat.seat_type,
                "base_price": show.base_price,
                "computed_price": computed_price,
                "status": seat_status,
                "held_by_me": held_by_me,
                "remaining_ttl_seconds": remaining_ttl,
            }

            if seat.row_label not in rows_dict:
                rows_dict[seat.row_label] = []
            rows_dict[seat.row_label].append(seat_data)

        matrix_rows = []
        for r_label, r_seats in rows_dict.items():
            primary_type = r_seats[0]["seat_type"] if r_seats else "STANDARD"
            matrix_rows.append({
                "row_label": r_label,
                "seat_type": primary_type,
                "seats": r_seats,
            })

        return {
            "show_id": show.id,
            "content_title": show.content.title if show.content else "Unknown",
            "theater_name": screen.theater.name if screen and screen.theater else "Unknown",
            "screen_name": screen.name if screen else "Screen",
            "start_time": show.start_time,
            "end_time": show.end_time,
            "base_price": show.base_price,
            "is_weekend": is_weekend,
            "is_prime_time": is_prime,
            "rows": matrix_rows,
            "total_available": total_available,
            "total_held": total_held,
            "total_booked": total_booked,
        }

    @staticmethod
    async def hold_seats(
        show_id: int,
        seat_ids: List[int],
        user_id: str,
        db: AsyncSession,
    ) -> Dict[str, Any]:
        if not seat_ids:
            raise HTTPException(status_code=400, detail="No seats requested for hold")
        if len(seat_ids) > 6:
            raise HTTPException(status_code=400, detail="Maximum 6 seats can be held at once")

        # 1. Check if show exists
        show = await db.get(Show, show_id)
        if not show:
            raise HTTPException(status_code=404, detail="Show not found")

        # 2. Check if any seat is permanently BOOKED in PostgreSQL
        booked_res = await db.execute(
            select(BookingSeat.seat_id)
            .join(Booking, BookingSeat.booking_id == Booking.id)
            .where(
                BookingSeat.show_id == show_id,
                BookingSeat.seat_id.in_(seat_ids),
                Booking.status == BookingStatus.PAID
            )
        )
        already_booked = booked_res.scalars().all()
        if already_booked:
            chaos_service.increment_contention()
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail={
                    "message": "Selected seats are already permanently booked.",
                    "conflicting_seat_ids": list(already_booked),
                }
            )

        # 3. Attempt atomic lock in Redis
        success, conflicts = await acquire_atomic_seat_locks(
            show_id=show_id,
            seat_ids=seat_ids,
            user_id=user_id,
        )

        if not success:
            chaos_service.increment_contention()
            logger.warning(f"Seat hold conflict on show {show_id}, conflicting seats: {conflicts} for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail={
                    "message": "Seats are currently held by another user. Please choose alternative seats.",
                    "conflicting_seat_ids": conflicts,
                }
            )

        return {
            "success": True,
            "show_id": show_id,
            "locked_seat_ids": seat_ids,
            "conflicting_seat_ids": [],
            "ttl_seconds": 600,
            "message": f"Successfully locked {len(seat_ids)} seats for 10 minutes."
        }

    @staticmethod
    async def release_holds(
        show_id: int,
        seat_ids: Optional[List[int]],
        user_id: str,
    ) -> Dict[str, Any]:
        released_count = await release_seat_locks(show_id, seat_ids, user_id)
        return {
            "success": True,
            "show_id": show_id,
            "released_count": released_count,
            "message": f"Released {released_count} seat holds."
        }
