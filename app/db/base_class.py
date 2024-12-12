from typing import Optional

from pydantic import BaseModel, Field
from bson import ObjectId


class MongoBaseModel(BaseModel):
    id: Optional[ObjectId] = Field(alias='_id', default=None)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        arbitrary_types_allowed = True
