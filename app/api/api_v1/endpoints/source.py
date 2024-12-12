from typing import Dict

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.deps import get_database, get_auth_user
from app.crud.source import CRUDSource
from app.schemas.source import (
    DummySourceOneContent,
    DummySourceOneContentUpdate, DummySourceTwoContentUpdate,
    DummySourceOneContentInDBBase, DummySourceTwoContentInDBBase
)
from app.core.auth import JWTBearer
from app.schemas.user import User

router = APIRouter()


@router.post('/webhook/dummy_source_1')
async def webhook(source_data: DummySourceOneContentUpdate, db: AsyncIOMotorClient = Depends(get_database)):
    _ = await CRUDSource(db).create(source_data)
    return {}


@router.post('/webhook/dummy_source_2')
async def webhook(source_data: DummySourceTwoContentUpdate, db: AsyncIOMotorClient = Depends(get_database)):
    _ = await CRUDSource(db).create(DummySourceOneContentUpdate(**source_data.dict()))
    return {}


@router.get('/my-topics', dependencies=[Depends(JWTBearer())], response_model=Dict)
async def my_topics(
        page: int = 1, page_size: int = 20,
        user: User = Depends(get_auth_user), db: AsyncIOMotorClient = Depends(get_database)
):
    docs = await CRUDSource(db).get_multi(
        skip=page_size*(page-1), limit=page_size, sort_by='created_at', stream=str(user.id))

    return {
        "page": page,
        "page_size": page_size,
        "total_results": len(docs),
        "results": list(docs),
    }
