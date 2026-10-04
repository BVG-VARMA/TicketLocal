from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.models import ContentType, SeatType, BookingStatus

# ----------------- AUTH SCHEMAS -----------------
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None

# ----------------- CATALOG SCHEMAS -----------------
class CityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

class ContentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    type: ContentType
    title: str
    description: str
    language: str
    genre: str
    duration_min: int
    poster_url: Optional[str] = None
    rating: float

class ScreenSimpleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    rows: int
    cols: int

class TheaterSimpleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    address: str
    city_id: int

class ShowOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    screen_id: int
    content_id: int
    start_time: datetime
    end_time: datetime
    base_price: float
    is_active: bool
    screen: Optional[ScreenSimpleOut] = None
    theater: Optional[TheaterSimpleOut] = None
    content: Optional[ContentOut] = None

class TheaterShowsOut(BaseModel):
    theater_id: int
    theater_name: str
    theater_address: str
    shows: List[ShowOut]

# ----------------- SEAT & LOCKING SCHEMAS -----------------
class SeatItem(BaseModel):
    id: int
    screen_id: int
    row_label: str
    seat_number: int
    seat_type: SeatType
    base_price: float
    computed_price: float
    status: str  # AVAILABLE, HELD, BOOKED
    held_by_me: bool = False
    remaining_ttl_seconds: Optional[int] = None

class SeatRow(BaseModel):
    row_label: str
    seat_type: SeatType
    seats: List[SeatItem]

class SeatMatrixResponse(BaseModel):
    show_id: int
    content_title: str
    theater_name: str
    screen_name: str
    start_time: datetime
    end_time: datetime
    base_price: float
    is_weekend: bool
    is_prime_time: bool
    rows: List[SeatRow]
    total_available: int
    total_held: int
    total_booked: int

class SeatHoldRequest(BaseModel):
    seat_ids: List[int] = Field(..., min_length=1, max_length=6)

class SeatHoldResponse(BaseModel):
    success: bool
    show_id: int
    locked_seat_ids: List[int]
    conflicting_seat_ids: List[int] = []
    ttl_seconds: int = 600
    message: str

class SeatReleaseRequest(BaseModel):
    seat_ids: Optional[List[int]] = None

# ----------------- CART & CHECKOUT SCHEMAS -----------------
class CartQuoteRequest(BaseModel):
    show_id: int
    seat_ids: List[int] = Field(..., min_length=1, max_length=6)

class SeatPriceBreakdown(BaseModel):
    seat_id: int
    row_label: str
    seat_number: int
    seat_type: SeatType
    price: float

class CartQuoteResponse(BaseModel):
    show_id: int
    seats: List[SeatPriceBreakdown]
    subtotal: float
    convenience_fee: float
    convenience_fee_percentage: float
    tax: float
    tax_percentage: float
    total: float
    holds_valid: bool
    min_remaining_ttl: Optional[int] = None

class PaymentCardInput(BaseModel):
    card_number: str = Field(..., min_length=12, max_length=19)
    card_holder: str = Field(..., min_length=2)
    expiry_month: str = Field(..., min_length=2, max_length=2)
    expiry_year: str = Field(..., min_length=2, max_length=4)
    cvv: str = Field(..., min_length=3, max_length=4)

class CheckoutRequest(BaseModel):
    show_id: int
    seat_ids: List[int] = Field(..., min_length=1, max_length=6)
    payment: PaymentCardInput

class TicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    booking_id: int
    qr_path: str
    qr_url: str
    issued_at: datetime

class BookingSeatOut(BaseModel):
    seat_id: int
    row_label: str
    seat_number: int
    seat_type: SeatType
    price: float

class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    show_id: int
    status: BookingStatus
    subtotal: float
    convenience_fee: float
    tax: float
    total: float
    created_at: datetime
    content_title: Optional[str] = None
    theater_name: Optional[str] = None
    screen_name: Optional[str] = None
    start_time: Optional[datetime] = None
    seats: List[BookingSeatOut] = []
    ticket: Optional[TicketOut] = None

# ----------------- CHAOS & METRICS SCHEMAS -----------------
class ChaosStatusResponse(BaseModel):
    chaos_enabled: bool
    tax_crash_active: bool
    db_lock_active: bool
    message: str

class MetricsLiteResponse(BaseModel):
    active_redis_locks: int
    seat_contention_count_423: int
    checkout_success_count: int
    checkout_failed_count: int
    checkout_abandonment_rate: float
    uptime_seconds: float
