from bson import ObjectId
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from app.db.base_class import MongoBaseModel

CollectionType = TypeVar("CollectionType", bound=MongoBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[CollectionType, CreateSchemaType, UpdateSchemaType]):
    model = None

    def __init__(self, db: AsyncIOMotorClient):
        self.collection = getattr(db, self.model.__collection__)

    async def get(self, _id: Union[ObjectId, str]) -> Optional[CollectionType]:
        if isinstance(_id, str):
            _id = ObjectId(_id)
        return self.model(**await self.collection.find_one({'_id': _id}))

    async def get_multi(self, skip: int = 0, limit: int = 20, sort_by: str = '', **kwargs) -> List[CollectionType]:
        docs = self.collection.find(kwargs).sort(sort_by, -1).skip(skip).limit(limit)
        return [self.model(**doc) async for doc in docs]

    async def create(self, obj_in: CreateSchemaType) -> Optional[CollectionType]:
        doc_data = obj_in.dict(by_alias=True, exclude_none=True)
        doc_data['created_at'] = datetime.now()
        insert_result = await self.collection.insert_one(doc_data)
        return await self.get(insert_result.inserted_id)

    async def update(
            self, db_obj: CollectionType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> CollectionType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        _ = await self.collection.update_one({'_id': db_obj.id}, {'$set': update_data})
        return await self.get(db_obj.id)

    async def remove(self, obj: Union[ObjectId, CollectionType]) -> None:
        if not isinstance(obj, ObjectId):
            obj = obj.id
        await self.collection.delete_one({'_id': obj})
