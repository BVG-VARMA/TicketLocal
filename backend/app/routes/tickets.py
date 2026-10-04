from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Booking, BookingSeat, Seat, Show, Screen, Theater, Movie, User
from app.schemas import TicketOut

router = APIRouter(prefix="/tickets", tags=["Ticket Verification"])

@router.get("/{booking_ref}", response_model=TicketOut)
async def get_ticket(booking_ref: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieves full booking details and local QR code path for a confirmed ticket.
    """
    query = (
        select(Booking)
        .where(Booking.booking_ref == booking_ref)
        .options(
            joinedload(Booking.user),
            joinedload(Booking.show).joinedload(Show.movie),
            joinedload(Booking.show).joinedload(Show.screen).joinedload(Screen.theater),
            joinedload(Booking.booking_seats).joinedload(BookingSeat.seat),
        )
    )
    res = await db.execute(query)
    booking = res.unique().scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Ticket not found")

    seats = [f"{bs.seat.row}{bs.seat.number}" for bs in booking.booking_seats if bs.seat]

    return {
        "booking_ref": booking.booking_ref,
        "status": booking.status,
        "movie_title": booking.show.movie.title if booking.show and booking.show.movie else "Unknown",
        "movie_poster": booking.show.movie.poster_url if booking.show and booking.show.movie else "",
        "theater_name": booking.show.screen.theater.name if booking.show and booking.show.screen and booking.show.screen.theater else "Unknown",
        "theater_address": booking.show.screen.theater.address if booking.show and booking.show.screen and booking.show.screen.theater else "",
        "screen_name": booking.show.screen.name if booking.show and booking.show.screen else "Screen",
        "show_date": booking.show.show_date if booking.show else "",
        "show_time": booking.show.start_time if booking.show else "",
        "format": booking.show.format if booking.show else "Standard",
        "language": booking.show.language if booking.show else "English",
        "seats": seats,
        "customer_name": booking.user.full_name if booking.user else "Valued Guest",
        "customer_email": booking.user.email if booking.user else "",
        "base_amount": booking.base_amount,
        "convenience_fee": booking.convenience_fee,
        "tax_amount": booking.tax_amount,
        "total_amount": booking.total_amount,
        "payment_method": booking.payment_method,
        "payment_id": booking.payment_id,
        "ticket_qr_url": booking.ticket_qr_path or "",
        "created_at": booking.created_at.isoformat() + "Z",
    }
