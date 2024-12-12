import pytest
import mongomock_motor
from bson import ObjectId

from app.crud.base import CRUDBase
from app.models import User, DummySourceOneContent
from app.schemas import UserCreate, UserUpdate, DummySourceOneContentCreate, DummySourceOneContentUpdate


@pytest.fixture
def mock_db():
    mock_client = mongomock_motor.AsyncMongoMockClient()
    return mock_client.get_database("test_db")


@pytest.fixture
def user_crud(mock_db):
    class MockCRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
        model = User
    return MockCRUDUser(mock_db)


@pytest.fixture
def dummy_source_crud(mock_db):
    class MockCRUDSource(CRUDBase[DummySourceOneContent, DummySourceOneContentCreate, DummySourceOneContentUpdate]):
        model = DummySourceOneContent
    return MockCRUDSource(mock_db)


@pytest.mark.asyncio
async def test_create_user(user_crud):
    user_data = UserCreate(email="test@example.com")

    created_user = await user_crud.create(user_data)

    assert created_user.email == user_data.email
    assert isinstance(created_user.id, ObjectId)


@pytest.mark.asyncio
async def test_get_user(user_crud):
    user_data = UserCreate(email="get_test@example.com")
    created_user = await user_crud.create(user_data)

    fetched_user = await user_crud.get(created_user.id)

    assert fetched_user.id == created_user.id
    assert fetched_user.email == created_user.email


@pytest.mark.asyncio
async def test_update_user(user_crud):
    user_data = UserCreate(email="update_test@example.com")
    created_user = await user_crud.create(user_data)

    updated_user = await user_crud.update(
        created_user, {"email": "updated_email@example.com"}
    )

    assert updated_user.email == "updated_email@example.com"


@pytest.mark.asyncio
async def test_remove_user(user_crud):
    user_data = UserCreate(email="delete_test@example.com")
    created_user = await user_crud.create(user_data)

    await user_crud.remove(created_user)

    fetched_user = await user_crud.get(created_user.id)
    assert fetched_user is None


@pytest.mark.asyncio
async def test_dummy_source_get_topic(dummy_source_crud):
    content_data = DummySourceOneContentCreate(
        topic="test_topic", data="test_data",
        stream="test_stream", image="test_image_url"
    )
    created_content = await dummy_source_crud.create(content_data)

    topics = await dummy_source_crud.get_multi(topic="test_topic")

    assert len(topics) == 1
    assert topics[0].topic == "test_topic"
