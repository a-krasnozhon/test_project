from datetime import datetime
from typing import List, Optional

from app.db.base_class import MongoBaseModel

from pydantic import EmailStr


class User(MongoBaseModel):
    __collection__ = 'users'

    email: EmailStr
    username: Optional[str]
    topics: Optional[List[str]]

    created_at: datetime
