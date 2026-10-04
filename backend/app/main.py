import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from app.config import settings
from app.db import engine, Base, AsyncSessionLocal
from app.seed import seed_database
from app.routers import (
    auth_router,
    catalog_router,
    seats_router,
    checkout_router,
    bookings_router,
    tickets_router,
    chaos_router,
    metrics_router,
)

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ticketlocal.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Startup: Initialize tables and seed
    logger.info("Initializing TicketLocal database tables...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        async with AsyncSessionLocal() as session:
            await seed_database(session)
    except Exception as e:
        logger.warning(f"Initial DB connect issue ({e}), re-initializing with local SQLite storage...")
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
        from app import db as app_db
        sqlite_url = f"sqlite+aiosqlite:///{settings.BASE_DIR}/ticketlocal.db"
        app_db.engine = create_async_engine(sqlite_url, connect_args={"check_same_thread": False}, pool_pre_ping=True)
        app_db.AsyncSessionLocal = async_sessionmaker(bind=app_db.engine, class_=AsyncSession, expire_on_commit=False)
        async with app_db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        async with app_db.AsyncSessionLocal() as session:
            await seed_database(session)

    logger.info("TicketLocal backend is operational and ready.")

    yield

    logger.info("Shutting down TicketLocal services...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="TicketLocal — Production-style Movie and Live Event Ticketing Engine (BookMyShow / District clone).",
    lifespan=lifespan,
)

# CORS middleware for frontend Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount local storage for ticket QR codes and assets
settings.TICKETS_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/storage", StaticFiles(directory=str(settings.STORAGE_DIR)), name="storage")

# Mount API routers under prefix
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(catalog_router, prefix=settings.API_V1_STR)
app.include_router(seats_router, prefix=settings.API_V1_STR)
app.include_router(checkout_router, prefix=settings.API_V1_STR)
app.include_router(bookings_router, prefix=settings.API_V1_STR)
app.include_router(tickets_router, prefix=settings.API_V1_STR)
app.include_router(chaos_router, prefix=settings.API_V1_STR)
app.include_router(metrics_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "ONLINE",
        "docs_url": "/docs",
        "api_v1": settings.API_V1_STR,
    }
