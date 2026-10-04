from app.routes.auth import router as auth_router
from app.routes.catalog import router as catalog_router
from app.routes.seats import router as seats_router
from app.routes.checkout import router as checkout_router
from app.routes.tickets import router as tickets_router
from app.routes.admin import router as admin_router

__all__ = [
    "auth_router",
    "catalog_router",
    "seats_router",
    "checkout_router",
    "tickets_router",
    "admin_router",
]

