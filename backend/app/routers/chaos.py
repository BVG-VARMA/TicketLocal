import asyncio
import logging
import qrcode
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.db import get_db
from app.redis_client import flush_all_seat_locks
from app.services.chaos_service import chaos_service
from app.schemas import ChaosStatusResponse

logger = logging.getLogger("ticketlocal.chaos")
router = APIRouter(prefix="/chaos", tags=["Chaos Lab"])

def check_chaos_enabled():
    if not settings.ENABLE_CHAOS:
        raise HTTPException(status_code=403, detail="Chaos Lab is disabled in production.")

@router.get("/status", response_model=ChaosStatusResponse)
async def get_chaos_status():
    check_chaos_enabled()
    return {
        "chaos_enabled": settings.ENABLE_CHAOS,
        "tax_crash_active": chaos_service.tax_crash_enabled,
        "db_lock_active": chaos_service.db_lock_enabled,
        "message": "Chaos Lab is active.",
    }

@router.post("/redis-drop")
async def drop_redis_locks():
    """
    Simulates total cache failure by dropping all seat locks.
    Database UNIQUE constraint will continue to guard against double-booking.
    """
    check_chaos_enabled()
    deleted_count = await flush_all_seat_locks()
    logger.warning(f"[CHAOS INJECTION] Dropped {deleted_count} active Redis seat locks!")
    return {
        "success": True,
        "dropped_locks": deleted_count,
        "message": f"Wiped {deleted_count} active seat locks from Redis cache.",
    }

@router.post("/db-lock")
async def lock_db_table(
    sleep_seconds: int = Query(5, ge=1, le=30, description="Lock duration in seconds"),
    db: AsyncSession = Depends(get_db),
):
    """
    Simulates heavy database row/table lock contention.
    """
    check_chaos_enabled()
    chaos_service.db_lock_enabled = True
    logger.warning(f"[CHAOS INJECTION] Holding DB transaction lock for {sleep_seconds}s...")
    try:
        # Acquire table lock
        is_sqlite = settings.DATABASE_URL.startswith("sqlite")
        if not is_sqlite:
            await db.execute(text("LOCK TABLE shows IN ACCESS EXCLUSIVE MODE;"))
        await asyncio.sleep(sleep_seconds)
        await db.commit()
    except Exception as e:
        await db.rollback()
        logger.error(f"DB lock exception: {e}")
    finally:
        chaos_service.db_lock_enabled = False

    return {
        "success": True,
        "sleep_seconds": sleep_seconds,
        "message": f"Released DB lock after {sleep_seconds}s.",
    }

@router.post("/tax-crash")
async def toggle_tax_crash(enable: bool = Query(True, description="Enable or disable tax calculation crash")):
    """
    Toggles ZeroDivisionError fault in tax calculator to test 500 error boundary.
    """
    check_chaos_enabled()
    chaos_service.tax_crash_enabled = enable
    logger.warning(f"[CHAOS INJECTION] Tax crash set to {enable}")
    return {
        "success": True,
        "tax_crash_active": chaos_service.tax_crash_enabled,
        "message": f"Tax crash fault injection {'ENABLED' if enable else 'DISABLED'}.",
    }

@router.post("/qr-storm")
async def simulate_qr_storm(
    count: int = Query(200, ge=10, le=1000, description="Number of dense QRs to generate synchronously")
):
    """
    Generates a dense batch of QR codes synchronously in the event loop to demonstrate blocking.
    """
    check_chaos_enabled()
    logger.warning(f"[CHAOS INJECTION] Starting QR storm of {count} synchronous generations...")
    for i in range(count):
        qr = qrcode.QRCode(version=3, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8, border=2)
        qr.add_data(f"CHAOS-STORM-STRESS-TEST-BLOCKING-PAYLOAD-{i}-" * 5)
        qr.make(fit=True)
        _ = qr.make_image()

    logger.warning(f"[CHAOS INJECTION] Completed QR storm of {count} codes.")
    return {
        "success": True,
        "generated_count": count,
        "message": f"Simulated synchronous QR storm of {count} items.",
    }

@router.post("/reset")
async def reset_all_chaos():
    """
    Resets all chaos fault injections to normal.
    """
    check_chaos_enabled()
    chaos_service.reset_chaos()
    logger.info("[CHAOS] Reset all fault injections to default.")
    return {
        "success": True,
        "tax_crash_active": False,
        "db_lock_active": False,
        "message": "All chaos fault injections have been reset.",
    }
