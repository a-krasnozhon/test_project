from app.crud.base import CRUDBase
from app.models import Stream
from app.schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[Stream, UserCreate, UserUpdate]):
    model = Stream

    async def get_user_by_email(self, email: str):
        return await self.collection.find_one({'email': email})
