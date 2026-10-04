import enum
from datetime import datetime
from typing import List, Optional, Any, Dict
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, DateTime,
    ForeignKey, UniqueConstraint, Index, Enum as SQLEnum, JSON
)
from sqlalchemy.orm import relationship
from app.db import Base

class ContentType(str, enum.Enum):
    MOVIE = "MOVIE"
    EVENT = "EVENT"

class SeatType(str, enum.Enum):
    STANDARD = "STANDARD"
    PREMIUM = "PREMIUM"
    RECLINER = "RECLINER"

class BookingStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, index=True, nullable=False)

    theaters = relationship("Theater", back_populates="city", cascade="all, delete-orphan")

class Theater(Base):
    __tablename__ = "theaters"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    address = Column(String(300), nullable=False)

    city = relationship("City", back_populates="theaters")
    screens = relationship("Screen", back_populates="theater", cascade="all, delete-orphan")

class Screen(Base):
    __tablename__ = "screens"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    theater_id = Column(Integer, ForeignKey("theaters.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    rows = Column(Integer, nullable=False, default=10)
    cols = Column(Integer, nullable=False, default=12)
    layout_config = Column(JSON, nullable=True)  # custom row-type mappings or aisle definitions

    theater = relationship("Theater", back_populates="screens")
    seats = relationship("Seat", back_populates="screen", cascade="all, delete-orphan")
    shows = relationship("Show", back_populates="screen", cascade="all, delete-orphan")

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    screen_id = Column(Integer, ForeignKey("screens.id", ondelete="CASCADE"), nullable=False, index=True)
    row_label = Column(String(10), nullable=False)
    seat_number = Column(Integer, nullable=False)
    seat_type = Column(SQLEnum(SeatType), nullable=False, default=SeatType.STANDARD)

    screen = relationship("Screen", back_populates="seats")
    booking_seats = relationship("BookingSeat", back_populates="seat")

    __table_args__ = (
        UniqueConstraint("screen_id", "row_label", "seat_number", name="uq_screen_row_seat"),
        Index("idx_seat_screen_row", "screen_id", "row_label"),
    )

class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(SQLEnum(ContentType), nullable=False, default=ContentType.MOVIE)
    title = Column(String(250), nullable=False, index=True)
    description = Column(Text, nullable=False)
    language = Column(String(50), nullable=False, default="English")
    genre = Column(String(100), nullable=False)
    duration_min = Column(Integer, nullable=False, default=120)
    poster_url = Column(String(500), nullable=True)
    rating = Column(Float, nullable=False, default=8.5)

    shows = relationship("Show", back_populates="content", cascade="all, delete-orphan")

class Show(Base):
    __tablename__ = "shows"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    screen_id = Column(Integer, ForeignKey("screens.id", ondelete="CASCADE"), nullable=False, index=True)
    content_id = Column(Integer, ForeignKey("content.id", ondelete="CASCADE"), nullable=False, index=True)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False)
    base_price = Column(Float, nullable=False, default=150.0)
    is_active = Column(Boolean, nullable=False, default=True)

    screen = relationship("Screen", back_populates="shows")
    content = relationship("Content", back_populates="shows")
    bookings = relationship("Booking", back_populates="show", cascade="all, delete-orphan")
    booking_seats = relationship("BookingSeat", back_populates="show", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_show_screen_time", "screen_id", "start_time"),
        Index("idx_show_content_active", "content_id", "is_active"),
    )

class PricingRule(Base):
    __tablename__ = "pricing_rules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    seat_type = Column(SQLEnum(SeatType), unique=True, nullable=False)
    multiplier = Column(Float, nullable=False, default=1.0)
    weekend_surge = Column(Float, nullable=False, default=1.25)
    prime_time_surge = Column(Float, nullable=False, default=1.15)

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    show_id = Column(Integer, ForeignKey("shows.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(SQLEnum(BookingStatus), nullable=False, default=BookingStatus.PENDING, index=True)
    subtotal = Column(Float, nullable=False, default=0.0)
    convenience_fee = Column(Float, nullable=False, default=0.0)
    tax = Column(Float, nullable=False, default=0.0)
    total = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="bookings")
    show = relationship("Show", back_populates="bookings")
    booking_seats = relationship("BookingSeat", back_populates="booking", cascade="all, delete-orphan")
    ticket = relationship("Ticket", back_populates="booking", uselist=False, cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_booking_user_status", "user_id", "status"),
    )

class BookingSeat(Base):
    __tablename__ = "booking_seats"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False, index=True)
    show_id = Column(Integer, ForeignKey("shows.id", ondelete="CASCADE"), nullable=False, index=True)
    seat_id = Column(Integer, ForeignKey("seats.id", ondelete="CASCADE"), nullable=False, index=True)
    price = Column(Float, nullable=False)

    booking = relationship("Booking", back_populates="booking_seats")
    show = relationship("Show", back_populates="booking_seats")
    seat = relationship("Seat", back_populates="booking_seats")

    __table_args__ = (
        UniqueConstraint("show_id", "seat_id", name="uq_show_seat_booking"),
        Index("idx_booking_seats_show", "show_id"),
        Index("idx_booking_seats_booking", "booking_id"),
    )

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    qr_path = Column(String(500), nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    booking = relationship("Booking", back_populates="ticket")

__all__ = [
    "ContentType",
    "SeatType",
    "BookingStatus",
    "User",
    "City",
    "Theater",
    "Screen",
    "Seat",
    "Content",
    "Show",
    "PricingRule",
    "Booking",
    "BookingSeat",
    "Ticket",
]
