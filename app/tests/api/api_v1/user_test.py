import pytest

from httpx import AsyncClient
from app.main import app
from motor.motor_asyncio import AsyncIOMotorClient

from app.crud.user import CRUDUser
from app.schemas.user import UserCreate
from app.crud.source import CRUDSource


@pytest.fixture
async def mock_db():
    mock_client = AsyncIOMotorClient("mongodb://localhost:27017/test_db")
    yield mock_client
    mock_client.close()


@pytest.fixture
async def test_app(mock_db):
    app.database = mock_db
    yield app


@pytest.fixture
async def async_client(test_app):
    async with AsyncClient(app=test_app, base_url="http://test/api/v1") as client:
        yield client


@pytest.mark.asyncio
async def test_register_user(async_client, mock_db):
    payload = {"email": "test@example.com"}

    response = await async_client.post("/user/register", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_user(async_client, mock_db):
    user = UserCreate(email="test@example.com")
    await CRUDUser(mock_db).create(user)

    response = await async_client.post("/user/login", json={"email": user.email})

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
