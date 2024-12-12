from datetime import datetime
from typing import List, Dict, Optional

from app.db.base_class import MongoBaseModel

from pydantic import EmailStr


class User(MongoBaseModel):
    __collection__ = 'users'

    email: EmailStr
    username: Optional[str]
    sources: Optional[Dict[str, List[str]]] = dict()

    created_at: datetime
