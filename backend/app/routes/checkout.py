import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.payment_service import PaymentService
from app.schemas import (
    FeeCalculationRequest, FeeBreakdownOut,
    CheckoutRequest, CheckoutResponse
)

logger = logging.getLogger("ticketlocal.checkout")

router = APIRouter(prefix="/checkout", tags=["Payment Simulator & Checkout"])

@router.post("/calculate", response_model=FeeBreakdownOut)
async def calculate_cart_fees(
    req: FeeCalculationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    FR3.1: Cart total = base seat price + convenience fee (10%) + local taxes (18% GST).
    """
    return await PaymentService.calculate_fees(show_id=req.show_id, seat_ids=req.seat_ids, db=db)

@router.post("/pay", response_model=CheckoutResponse)
async def process_checkout(
    req: CheckoutRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    FR3.2: POST /api/checkout accepts mock payment details, simulates 2000ms delay, then processes.
    FR3.3: On success, run a Postgres transaction converting Redis HELD -> permanent Postgres BOOKED state.
    FR3.4: Generate a local PNG QR code with payload (ticket_id, status: PAID) and return file path.
    """
    return await PaymentService.process_checkout(
        show_id=req.show_id,
        seat_ids=req.seat_ids,
        user_id=req.user_id,
        customer_name=req.customer_name,
        customer_email=req.customer_email,
        customer_phone=req.customer_phone or "9876543210",
        payment_method=req.payment_method,
        db=db,
    )
