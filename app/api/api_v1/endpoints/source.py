import logging

from logging import INFO
from typing import Dict

import httpx
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.deps import get_database, get_auth_user
from app.crud.source import CRUDSource
from app.schemas.source import (
    DummySourceOneContent, DummySourceOneContentCreate,
    DummySourceOneContentUpdate, DummySourceTwoContentUpdate,
    DummySourceOneContentInDBBase, DummySourceTwoContentInDBBase
)
from app.sources.source_one import DummySourceOne
from app.core.auth import JWTBearer
from app.schemas.user import User

router = APIRouter()

logging.getLogger('root').setLevel('INFO')
logging.lastResort.setLevel(INFO)



@router.post('/webhook/dummy_source_1')
async def webhook(source_data: DummySourceOneContentCreate, db: AsyncIOMotorClient = Depends(get_database)):
    _ = await CRUDSource(db).create(source_data)
    return {}


@router.post('/webhook/dummy_source_2')
async def webhook(source_data: DummySourceTwoContentUpdate, db: AsyncIOMotorClient = Depends(get_database)):
    _ = await CRUDSource(db).create(DummySourceOneContentCreate(**source_data.dict()))
    return {}


@router.get('/my-topics', dependencies=[Depends(JWTBearer())], response_model=Dict)
async def my_topics(
        page: int = 1, page_size: int = 20,
        user: User = Depends(get_auth_user), db: AsyncIOMotorClient = Depends(get_database)
):
    source = DummySourceOne()
    url = source.base_url + source.data_fetch_url
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url.format(stream=str(user.id)), params={'order': user.sources[source.name]})
            response.raise_for_status()
            data = response.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        logging.exception(exc)
        data = []

    for doc in data:
        _ = await CRUDSource(db).create(DummySourceOneContentCreate(**doc))

    docs = await CRUDSource(db).get_multi(
        skip=page_size*(page-1), limit=page_size, sort_by='created_at', stream=str(user.id))

    return {
        "page": page,
        "page_size": page_size,
        "total_results": len(docs),
        "results": list(docs),
    }
