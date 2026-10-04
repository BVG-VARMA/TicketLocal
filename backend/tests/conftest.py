import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.db import Base, get_db
from app.main import app
from app.models import User
from app.seed import seed_database
from app.services.auth_service import get_password_hash
from app.redis_client import flush_all_seat_locks

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope="function")
async def test_db_session():
    test_engine = create_async_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    TestSessionLocal = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)
    
    async with TestSessionLocal() as session:
        await seed_database(session)

        # Seed additional test users (IDs 3..65) for concurrency testing
        extra_users = []
        for i in range(3, 70):
            extra_users.append(
                User(
                    id=i,
                    name=f"Test User {i}",
                    email=f"testuser{i}@ticketlocal.com",
                    password_hash=get_password_hash("Test@1234"),
                )
            )
        session.add_all(extra_users)
        await session.commit()

    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    await flush_all_seat_locks()

    yield TestSessionLocal

    app.dependency_overrides.clear()
    await test_engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def client(test_db_session):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
