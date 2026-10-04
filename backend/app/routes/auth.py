import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User
from app.schemas import UserRegister, UserLogin, UserOut, TokenResponse, GuestSessionResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/guest", response_model=GuestSessionResponse)
async def create_guest_session():
    """
    Creates an instant guest session for quick seat locking and checkout.
    """
    guest_uuid = f"guest_{uuid.uuid4().hex[:8]}"
    return {
        "guest_id": guest_uuid,
        "guest_name": f"Guest {guest_uuid[-4:].upper()}"
    }

@router.post("/register", response_model=UserOut)
async def register_user(req: UserRegister, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User).where(User.email == req.email))
    if res.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(
        email=req.email,
        hashed_password=f"hashed_{req.password}",
        full_name=req.full_name,
        phone=req.phone,
        role="customer"
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/login", response_model=TokenResponse)
async def login_user(req: UserLogin, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User).where(User.email == req.email))
    user = res.scalar_one_or_none()
    if not user:
        # For seamless testing, auto-create user on first login
        user = User(
            email=req.email,
            hashed_password=f"hashed_{req.password}",
            full_name=req.email.split("@")[0].capitalize(),
            role="customer"
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
    return {
        "access_token": f"jwt_mock_token_{user.id}_{uuid.uuid4().hex[:8]}",
        "token_type": "bearer",
        "user": user
    }
