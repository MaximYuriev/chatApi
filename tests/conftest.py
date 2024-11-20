import asyncio

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB_TEST
from db.database import Base, get_session
from src.main import app

db_url_test = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_TEST}"

test_db_engine = create_async_engine(db_url_test, echo=False, poolclass=NullPool)
test_async_session = async_sessionmaker(test_db_engine, expire_on_commit=False)


async def override_get_session():
    async with test_async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with test_db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


async def create_two_user(client: AsyncClient):
    user = {
        "email": "testuser@example.com",
        "password": "string",
        "username": "test_user"
    }
    await client.post("/auth/registration", json=user)
    user.update(email="testuser2@example.com", username="test_user2")
    await client.post("/auth/registration", json=user)


@pytest.fixture
async def current_test_user(client: AsyncClient):
    await create_two_user(client)
    user = {
        "email": "testuser@example.com",
        "password": "string"
    }
    await client.post("/auth/login", json=user)
    yield client.cookies
