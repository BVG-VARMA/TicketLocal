from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.models import Booking, BookingSeat, Show, Screen, Theater, Content, Seat, Ticket, User
from app.schemas import BookingOut, BookingSeatOut, TicketOut
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.get("", response_model=List[BookingOut])
async def get_my_bookings(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Booking)
        .where(Booking.user_id == current_user.id)
        .options(
            joinedload(Booking.show).joinedload(Show.content),
            joinedload(Booking.show).joinedload(Show.screen).joinedload(Screen.theater),
            joinedload(Booking.booking_seats).joinedload(BookingSeat.seat),
            joinedload(Booking.ticket),
        )
        .order_by(Booking.created_at.desc())
    )
    res = await db.execute(query)
    bookings = res.unique().scalars().all()

    output = []
    for b in bookings:
        seats_list = []
        for bs in b.booking_seats:
            if bs.seat:
                seats_list.append(
                    BookingSeatOut(
                        seat_id=bs.seat_id,
                        row_label=bs.seat.row_label,
                        seat_number=bs.seat.seat_number,
                        seat_type=bs.seat.seat_type,
                        price=bs.price,
                    )
                )

        ticket_out = None
        if b.ticket:
            ticket_out = TicketOut(
                id=b.ticket.id,
                booking_id=b.ticket.booking_id,
                qr_path=b.ticket.qr_path,
                qr_url=f"/api/tickets/{b.ticket.id}/qr",
                issued_at=b.ticket.issued_at,
            )

        output.append(
            BookingOut(
                id=b.id,
                user_id=b.user_id,
                show_id=b.show_id,
                status=b.status,
                subtotal=b.subtotal,
                convenience_fee=b.convenience_fee,
                tax=b.tax,
                total=b.total,
                created_at=b.created_at,
                content_title=b.show.content.title if b.show and b.show.content else "Unknown Event",
                theater_name=b.show.screen.theater.name if b.show and b.show.screen and b.show.screen.theater else "Cinema",
                screen_name=b.show.screen.name if b.show and b.show.screen else "Screen",
                start_time=b.show.start_time if b.show else None,
                seats=seats_list,
                ticket=ticket_out,
            )
        )
    return output

@router.get("/{booking_id}", response_model=BookingOut)
async def get_booking_by_id(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Booking)
        .where(Booking.id == booking_id, Booking.user_id == current_user.id)
        .options(
            joinedload(Booking.show).joinedload(Show.content),
            joinedload(Booking.show).joinedload(Show.screen).joinedload(Screen.theater),
            joinedload(Booking.booking_seats).joinedload(BookingSeat.seat),
            joinedload(Booking.ticket),
        )
    )
    res = await db.execute(query)
    b = res.unique().scalar_one_or_none()
    if not b:
        raise HTTPException(status_code=404, detail="Booking not found")

    seats_list = []
    for bs in b.booking_seats:
        if bs.seat:
            seats_list.append(
                BookingSeatOut(
                    seat_id=bs.seat_id,
                    row_label=bs.seat.row_label,
                    seat_number=bs.seat.seat_number,
                    seat_type=bs.seat.seat_type,
                    price=bs.price,
                )
            )

    ticket_out = None
    if b.ticket:
        ticket_out = TicketOut(
            id=b.ticket.id,
            booking_id=b.ticket.booking_id,
            qr_path=b.ticket.qr_path,
            qr_url=f"/api/tickets/{b.ticket.id}/qr",
            issued_at=b.ticket.issued_at,
        )

    return BookingOut(
        id=b.id,
        user_id=b.user_id,
        show_id=b.show_id,
        status=b.status,
        subtotal=b.subtotal,
        convenience_fee=b.convenience_fee,
        tax=b.tax,
        total=b.total,
        created_at=b.created_at,
        content_title=b.show.content.title if b.show and b.show.content else "Unknown Event",
        theater_name=b.show.screen.theater.name if b.show and b.show.screen and b.show.screen.theater else "Cinema",
        screen_name=b.show.screen.name if b.show and b.show.screen else "Screen",
        start_time=b.show.start_time if b.show else None,
        seats=seats_list,
        ticket=ticket_out,
    )
