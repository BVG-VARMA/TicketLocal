import pytest
from datetime import datetime
from app.models import SeatType
from app.services.pricing_service import PricingService

def test_standard_seat_regular_hours():
    # Tuesday 14:00 (Weekday, Non-prime)
    dt = datetime(2026, 9, 15, 14, 0)
    assert not PricingService.is_weekend(dt)
    assert not PricingService.is_prime_time(dt)

    price = PricingService.calculate_seat_price(
        base_price=200.0,
        seat_type=SeatType.STANDARD,
        show_time=dt,
        type_multiplier=1.0,
        weekend_surge=1.25,
        prime_time_surge=1.15,
    )
    assert price == 200.0

def test_premium_and_recliner_multipliers():
    dt = datetime(2026, 9, 15, 14, 0)
    p_premium = PricingService.calculate_seat_price(
        base_price=200.0,
        seat_type=SeatType.PREMIUM,
        show_time=dt,
        type_multiplier=1.4,
    )
    assert p_premium == 280.0

    p_recliner = PricingService.calculate_seat_price(
        base_price=200.0,
        seat_type=SeatType.RECLINER,
        show_time=dt,
        type_multiplier=1.8,
    )
    assert p_recliner == 360.0

def test_weekend_surge():
    # Saturday 14:00
    dt = datetime(2026, 9, 19, 14, 0)
    assert PricingService.is_weekend(dt)
    assert not PricingService.is_prime_time(dt)

    price = PricingService.calculate_seat_price(
        base_price=200.0,
        seat_type=SeatType.STANDARD,
        show_time=dt,
        type_multiplier=1.0,
        weekend_surge=1.25,
        prime_time_surge=1.15,
    )
    assert price == 250.0  # 200 * 1.25

def test_prime_time_surge():
    # Wednesday 19:30 (Prime time 18:00 - 22:00)
    dt = datetime(2026, 9, 16, 19, 30)
    assert not PricingService.is_weekend(dt)
    assert PricingService.is_prime_time(dt)

    price = PricingService.calculate_seat_price(
        base_price=200.0,
        seat_type=SeatType.STANDARD,
        show_time=dt,
        type_multiplier=1.0,
        weekend_surge=1.25,
        prime_time_surge=1.15,
    )
    assert price == 230.0  # 200 * 1.15

def test_combined_weekend_and_prime_time():
    # Saturday 20:00 (Weekend AND Prime time)
    dt = datetime(2026, 9, 19, 20, 0)
    assert PricingService.is_weekend(dt)
    assert PricingService.is_prime_time(dt)

    price = PricingService.calculate_seat_price(
        base_price=200.0,
        seat_type=SeatType.PREMIUM,
        show_time=dt,
        type_multiplier=1.4,
        weekend_surge=1.25,
        prime_time_surge=1.15,
    )
    # 200 * 1.4 * 1.25 * 1.15 = 402.5
    assert price == 402.5

def test_order_fee_and_gst_tax_breakdown():
    subtotal = 500.0
    totals = PricingService.calculate_order_totals(
        subtotal=subtotal,
        fee_percentage=0.10,
        tax_percentage=0.18,
    )
    assert totals["subtotal"] == 500.0
    assert totals["convenience_fee"] == 50.0  # 10%
    assert totals["tax"] == 99.0  # 18% of (500 + 50) = 18% of 550 = 99.0
    assert totals["total"] == 649.0  # 500 + 50 + 99 = 649.0
