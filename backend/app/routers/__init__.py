from app.routers.auth import router as auth_router
from app.routers.catalog import router as catalog_router
from app.routers.seats import router as seats_router
from app.routers.checkout import router as checkout_router
from app.routers.bookings import router as bookings_router
from app.routers.tickets import router as tickets_router
from app.routers.chaos import router as chaos_router
from app.routers.metrics import router as metrics_router

__all__ = [
    "auth_router",
    "catalog_router",
    "seats_router",
    "checkout_router",
    "bookings_router",
    "tickets_router",
    "chaos_router",
    "metrics_router",
]
