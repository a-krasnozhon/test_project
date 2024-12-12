from typing import Union

from app.crud.base import CRUDBase
from app.models import User
from app.schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    model = User

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        doc = await self.collection.find_one({'email': email})
        if doc:
            return self.model(**doc)
        return None
