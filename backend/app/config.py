import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    PROJECT_NAME: str = "TicketLocal"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    ENABLE_CHAOS: bool = True
    API_V1_STR: str = "/api"

    # Base Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    STORAGE_DIR: Path = BASE_DIR / "storage"
    TICKETS_DIR: Path = BASE_DIR / "storage" / "tickets"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://ticketlocal:ticketlocal_secret@localhost:5432/ticketlocal_db"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_LOCK_TTL_SECONDS: int = 600

    # Auth
    SECRET_KEY: str = "ticketlocal-super-secret-jwt-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Pricing & Taxes
    CONVENIENCE_FEE_PERCENTAGE: float = 0.10
    GST_TAX_PERCENTAGE: float = 0.18
    PRIME_TIME_START_HOUR: int = 18
    PRIME_TIME_END_HOUR: int = 22
    WEEKEND_SURGE_MULTIPLIER: float = 1.25
    PRIME_TIME_SURGE_MULTIPLIER: float = 1.15

settings = Settings()

# Ensure directories exist
settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
settings.TICKETS_DIR.mkdir(parents=True, exist_ok=True)
