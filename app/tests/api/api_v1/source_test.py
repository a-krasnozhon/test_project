import pytest

from httpx import AsyncClient
from app.main import app
from motor.motor_asyncio import AsyncIOMotorClient

from app.crud.source import CRUDSource
from app.schemas.source import DummySourceOneContentCreate


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
async def test_webhook_dummy_source_1(async_client, mock_db):
    payload = {"topic": "test_topic", "data": "test_data", "stream": "test_stream", "image": "test_image_url"}

    response = await async_client.post("/source/webhook/dummy_source_1", json=payload)

    assert response.status_code == 200
    stored_data = await CRUDSource(mock_db).get_topic("test_topic")
    assert stored_data.topic == "test_topic"
