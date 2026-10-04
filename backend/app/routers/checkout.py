from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.models import User
from app.schemas import CartQuoteRequest, CartQuoteResponse, CheckoutRequest
from app.services.auth_service import get_current_user
from app.services.checkout_service import CheckoutService

router = APIRouter(tags=["Cart & Checkout"])

@router.post("/cart/quote", response_model=CartQuoteResponse)
async def get_quote(
    quote_req: CartQuoteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Computes pricing breakdown with convenience fees and GST tax.
    Validates that the user holds the locks in Redis.
    """
    return await CheckoutService.get_cart_quote(
        show_id=quote_req.show_id,
        seat_ids=quote_req.seat_ids,
        user_id=str(current_user.id),
        db=db,
    )

@router.post("/checkout")
async def checkout(
    checkout_req: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Executes mock payment (2s async sleep), verifies Redis holds, commits PostgreSQL
    booking transaction, generates QR ticket PNG, and clears holds.
    """
    return await CheckoutService.process_checkout(
        show_id=checkout_req.show_id,
        seat_ids=checkout_req.seat_ids,
        payment=checkout_req.payment,
        user_id=current_user.id,
        db=db,
    )
