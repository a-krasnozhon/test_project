from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app import models, crud
from app.schemas import UserCreate
from app.tests.utils.utils import random_email, random_lower_string


async def create_random_user(db: AsyncSession, **kwargs) -> models.User:
    user_in = UserCreate(
        email=random_email(),
        nickname=random_lower_string(),
    )

    for k, v in kwargs.items():
        setattr(user_in, k, v)

    return await crud.user.create(db=db, obj_in=user_in)
