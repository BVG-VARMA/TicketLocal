from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.models import User
from app.schemas import (
    SeatMatrixResponse, SeatHoldRequest, SeatHoldResponse, SeatReleaseRequest
)
from app.services.auth_service import get_current_user, get_current_user_optional
from app.services.seat_service import SeatService

router = APIRouter(prefix="/shows", tags=["Seats & Locking"])

@router.get("/{show_id}/seats", response_model=SeatMatrixResponse)
async def get_show_seats(
    show_id: int,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns 2D matrix of seats for the show with live status (AVAILABLE, HELD, BOOKED)
    and computed prices including surge multipliers.
    """
    user_id = str(current_user.id) if current_user else None
    return await SeatService.get_seat_matrix(show_id=show_id, user_id=user_id, db=db)

@router.post("/{show_id}/seats/hold", response_model=SeatHoldResponse)
async def hold_seats(
    show_id: int,
    hold_req: SeatHoldRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Atomically acquires temporary 600s TTL Redis locks for up to 6 seats.
    Returns HTTP 423 Locked with conflicting seat IDs if any seat is unavailable.
    """
    return await SeatService.hold_seats(
        show_id=show_id,
        seat_ids=hold_req.seat_ids,
        user_id=str(current_user.id),
        db=db,
    )

@router.delete("/{show_id}/seats/hold")
async def release_holds(
    show_id: int,
    release_req: Optional[SeatReleaseRequest] = None,
    current_user: User = Depends(get_current_user),
):
    """
    Explicitly releases temporary seat holds for the user.
    """
    seat_ids = release_req.seat_ids if release_req else None
    return await SeatService.release_holds(
        show_id=show_id,
        seat_ids=seat_ids,
        user_id=str(current_user.id),
    )
