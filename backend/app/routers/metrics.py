import logging
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.db import get_db
from app.redis_client import count_active_locks, redis_manager
from app.services.chaos_service import chaos_service
from app.schemas import MetricsLiteResponse

router = APIRouter(tags=["System & Metrics"])

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    db_ok = False
    try:
        await db.execute(text("SELECT 1;"))
        db_ok = True
    except Exception:
        pass

    redis_ok = False
    try:
        client = await redis_manager.get_client()
        await client.ping()
        redis_ok = True
    except Exception:
        pass

    return {
        "status": "HEALTHY" if (db_ok and redis_ok) else "DEGRADED",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": "CONNECTED" if db_ok else "DISCONNECTED",
        "redis": "CONNECTED" if redis_ok else "FALLBACK",
        "chaos_enabled": settings.ENABLE_CHAOS,
    }

@router.get("/metrics-lite", response_model=MetricsLiteResponse)
async def get_metrics_lite():
    active_locks = await count_active_locks()
    return MetricsLiteResponse(
        active_redis_locks=active_locks,
        seat_contention_count_423=chaos_service.contention_count_423,
        checkout_success_count=chaos_service.checkout_success_count,
        checkout_failed_count=chaos_service.checkout_failed_count,
        checkout_abandonment_rate=chaos_service.get_abandonment_rate(),
        uptime_seconds=chaos_service.get_uptime_seconds(),
    )
