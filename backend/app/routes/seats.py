from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.seat_service import SeatService
from app.schemas import (
    SeatMatrixOut, LockSeatsRequest, LockSeatsResponse,
    ReleaseSeatsRequest, ReleaseSeatsResponse
)

router = APIRouter(prefix="/shows", tags=["Seats & Locking Engine"])

@router.get("/{show_id}/seats", response_model=SeatMatrixOut)
async def get_show_seats(
    show_id: int,
    user_id: Optional[str] = Query(None, description="Current user/guest identifier"),
    db: AsyncSession = Depends(get_db)
):
    """
    FR1.1: Returns a 2D seat matrix (A1-A10, B1-B10, etc.) with live status:
    AVAILABLE, HELD, BOOKED along with remaining TTL.
    """
    return await SeatService.get_seat_matrix(show_id=show_id, user_id=user_id, db=db)

@router.post("/{show_id}/lock-seats", response_model=LockSeatsResponse)
async def lock_seats(
    show_id: int,
    req: LockSeatsRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    FR1.2: On seat selection, write Redis key (e.g. lock:show_123:seat_4) with 600-second TTL.
    FR1.3: If another user selects a held seat, return HTTP 423 Locked.
    FR1.4: If checkout isn't completed in 10 min, Redis auto-evicts key back to AVAILABLE.
    """
    return await SeatService.lock_seats(
        show_id=show_id,
        seat_ids=req.seat_ids,
        user_id=req.user_id,
        db=db
    )

@router.post("/{show_id}/release-seats", response_model=ReleaseSeatsResponse)
async def release_seats(
    show_id: int,
    req: ReleaseSeatsRequest
):
    """
    Releases held seats explicitly (e.g. user unselects seat or navigates back).
    """
    return await SeatService.release_seats(
        show_id=show_id,
        seat_ids=req.seat_ids,
        user_id=req.user_id
    )
