from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.utils.user import create_random_user
from app.core.config import settings


class TestUser:
    async def test_get_user(self, async_client: AsyncClient, db_session: AsyncSession):
        user = await create_random_user(db=db_session)

        response = await async_client.get(f"{settings.API_V1_STR}/user/")

        assert response.status_code == 200
