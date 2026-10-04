import time
from typing import Dict, Any

class ChaosService:
    def __init__(self):
        self.tax_crash_enabled: bool = False
        self.db_lock_enabled: bool = False
        self.db_lock_duration: int = 5
        self.start_time: float = time.time()

        # Metrics counters
        self.contention_count_423: int = 0
        self.checkout_success_count: int = 0
        self.checkout_failed_count: int = 0
        self.checkout_attempts_count: int = 0

    def increment_contention(self):
        self.contention_count_423 += 1

    def increment_checkout_attempt(self):
        self.checkout_attempts_count += 1

    def increment_checkout_success(self):
        self.checkout_success_count += 1

    def increment_checkout_failure(self):
        self.checkout_failed_count += 1

    def get_abandonment_rate(self) -> float:
        if self.checkout_attempts_count == 0:
            return 0.0
        abandoned = max(0, self.checkout_attempts_count - self.checkout_success_count)
        return round((abandoned / self.checkout_attempts_count) * 100.0, 2)

    def get_uptime_seconds(self) -> float:
        return round(time.time() - self.start_time, 1)

    def reset_chaos(self):
        self.tax_crash_enabled = False
        self.db_lock_enabled = False

chaos_service = ChaosService()
