import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    # Create database schema
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Drop database schema
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_db():
    async with AsyncSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.mark.asyncio
async def test_create_book():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/books", json={"title": "Test Book", "author": "Author 1", "summary": "Summary 1"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"


@pytest.mark.asyncio
async def test_get_books():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Add a book first
        await ac.post("/books", json={"title": "Test Book", "author": "Author 1", "summary": "Summary 1"})
        # Get books
        response = await ac.get("/books")
    assert response.status_code == 200
    assert len(response.json()) == 1
