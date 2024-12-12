from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.tests.utils.user import create_random_user


class TestCRUDUser:
    async def test_get_user_by_email(self, db_session: AsyncSession):
        user = await create_random_user(db_session)

        result = await crud.user.get_user_by_email(db=db_session, email=user.email)

        assert result
        assert result.id == user.id
