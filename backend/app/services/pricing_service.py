from datetime import datetime
from typing import Dict
from app.config import settings
from app.models import SeatType

DEFAULT_MULTIPLIERS = {
    SeatType.STANDARD: 1.0,
    SeatType.PREMIUM: 1.4,
    SeatType.RECLINER: 1.8,
}

class PricingService:
    @staticmethod
    def is_weekend(dt: datetime) -> bool:
        # Friday evening (>=18), Saturday (5), Sunday (6)
        # Saturday is 5, Sunday is 6
        return dt.weekday() in (5, 6)

    @staticmethod
    def is_prime_time(dt: datetime) -> bool:
        hour = dt.hour
        return settings.PRIME_TIME_START_HOUR <= hour < settings.PRIME_TIME_END_HOUR

    @classmethod
    def calculate_seat_price(
        cls,
        base_price: float,
        seat_type: SeatType,
        show_time: datetime,
        type_multiplier: float = None,
        weekend_surge: float = None,
        prime_time_surge: float = None,
    ) -> float:
        mult = type_multiplier if type_multiplier is not None else DEFAULT_MULTIPLIERS.get(seat_type, 1.0)
        w_surge = weekend_surge if weekend_surge is not None else settings.WEEKEND_SURGE_MULTIPLIER
        p_surge = prime_time_surge if prime_time_surge is not None else settings.PRIME_TIME_SURGE_MULTIPLIER

        price = base_price * mult

        if cls.is_weekend(show_time):
            price *= w_surge

        if cls.is_prime_time(show_time):
            price *= p_surge

        return round(price, 2)

    @classmethod
    def calculate_order_totals(
        cls,
        subtotal: float,
        fee_percentage: float = settings.CONVENIENCE_FEE_PERCENTAGE,
        tax_percentage: float = settings.GST_TAX_PERCENTAGE,
        force_tax_crash: bool = False,
    ) -> Dict[str, float]:
        if force_tax_crash:
            # Chaos lab fault injection
            _ = 1 / 0

        convenience_fee = round(subtotal * fee_percentage, 2)
        taxable_amount = subtotal + convenience_fee
        tax = round(taxable_amount * tax_percentage, 2)
        total = round(subtotal + convenience_fee + tax, 2)

        return {
            "subtotal": subtotal,
            "convenience_fee": convenience_fee,
            "convenience_fee_percentage": fee_percentage,
            "tax": tax,
            "tax_percentage": tax_percentage,
            "total": total,
        }
