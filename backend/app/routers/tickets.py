import os
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.models import Ticket, Booking, Show, Content, Screen, Theater
from app.schemas import TicketOut

router = APIRouter(prefix="/tickets", tags=["Tickets & QR"])

@router.get("/{ticket_id}", response_model=TicketOut)
async def get_ticket_info(ticket_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = res.scalar_one_or_none()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return TicketOut(
        id=ticket.id,
        booking_id=ticket.booking_id,
        qr_path=ticket.qr_path,
        qr_url=f"/api/tickets/{ticket.id}/qr",
        issued_at=ticket.issued_at,
    )

@router.get("/{ticket_id}/qr")
async def get_ticket_qr_image(ticket_id: int, db: AsyncSession = Depends(get_db)):
    """
    Serves the locally generated QR PNG ticket.
    """
    res = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = res.scalar_one_or_none()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    file_path = Path(ticket.qr_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="QR image file missing from local storage")

    return FileResponse(
        path=str(file_path),
        media_type="image/png",
        filename=f"ticket_{ticket.booking_id}.png"
    )
