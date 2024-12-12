from typing import Optional, List, Annotated, Any

from bson import ObjectId
from pydantic import BaseModel, Field

from app.core.utils import ObjectIdPydanticAnnotation


PyObjectId = Annotated[ObjectId, ObjectIdPydanticAnnotation]


class TokenBase(BaseModel):
    access_token: str
    token_type: str = 'Bearer'


class UserBase(BaseModel):
    email: str
    username: str = ''
    topics: Optional[List[str]] = []


class UserUpdate(BaseModel):
    username: str = ''
    topics: Optional[List[str]] = []


class UserCreate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: Optional[PyObjectId] = Field(default=None)

    class Config:
        json_encoders = {PyObjectId: str}
        populate_by_name = True
        arbitrary_types_allowed = True


class User(UserInDBBase):
    pass
