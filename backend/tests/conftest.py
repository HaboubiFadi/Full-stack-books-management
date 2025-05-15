import os 
import warnings 

from typing import AsyncGenerator

from unittest import mock

import pytest_asyncio 

from src import app 

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.orm import sessionmaker


from src.db.main import get_session

from fastapi.testclient import TestClient

from src.books.models import Book

from sqlmodel import SQLModel

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test_db.db"

async_engine = create_async_engine(
SQLALCHEMY_DATABASE_URL,
echo = True,
connect_args={"check_same_thread":False},

)

async_session = sessionmaker(bind=async_engine , expire_on_commit = False , class_ = AsyncSession)

async def initdb()-> None :
    async with async_engine.begin() as conn :
        await conn.run_sync(SQLModel.metadata.create_all)


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    await initdb()
    async with async_session() as  session :
        yield session
        
from httpx import ASGITransport, AsyncClient
import pytest
@pytest_asyncio.fixture(scope="function")
async def test_client(db_session) :
    def override_get_db():
        yield db_session
        
    app.dependency_overrides[get_session] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as test_client:
        yield test_client

import uuid
@pytest.fixture()
def book_uid() -> uuid.UUID :
    return str(uuid.uuid4())

@pytest.fixture
def book_payload() :
    """Generate a user payload."""
    return {
        "title": "Think C++",
        "author": "Allen B. Downey",
        "publisher": "O'Reilly Media",
        "published_date": "2021-01-01",
        "page_count": 1234,
        "language": "English"
}


