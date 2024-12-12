import httpx

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.deps import get_database, get_auth_user
from app.core.auth import JWTBearer
from app.core.utils import create_access_token
from app.crud.user import CRUDUser
from app.schemas.user import User, UserCreate, UserUpdate, TokenBase
from app.sources import available_sources

router = APIRouter()


@router.get("/", response_model=User)
async def get():
    pass


@router.post("/register", response_model=TokenBase)
async def register_user(user: UserCreate, db: AsyncIOMotorClient = Depends(get_database)):
    crud = CRUDUser(db)
    existing_user = await crud.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User exists")
    new_user = await crud.create(user)
    access_token = create_access_token(data={"sub": str(new_user.id)})

    return TokenBase(**{"access_token": access_token})


@router.post("/login", response_model=TokenBase)
async def login(user: UserCreate, db: AsyncIOMotorClient = Depends(get_database)):
    existing_user = await CRUDUser(db).get_user_by_email(user.email)
    print(existing_user)
    if not existing_user:
        raise HTTPException(status_code=400, detail="User does not exist")
    access_token = create_access_token(data={"sub": str(existing_user.id)})

    return TokenBase(**{"access_token": access_token})


@router.get("/my", dependencies=[Depends(JWTBearer())], response_model=User)
async def get_user(user: User = Depends(get_auth_user)):
    return user


@router.patch('/update', dependencies=[Depends(JWTBearer())], response_model=User)
async def update_user(
        background_tasks: BackgroundTasks,
        update_data: UserUpdate,
        user: User = Depends(get_auth_user),
        db: AsyncIOMotorClient = Depends(get_database),
):
    updated_user = await CRUDUser(db).update(user, update_data)
    new_sources = set(update_data.sources.keys())
    old_sources = set(user.sources.keys())
    if new_sources != old_sources:
        await toggle_subscription_to_streams(
            new_sources - old_sources,
            old_sources - new_sources,
            background_tasks,
            str(user.id)
        )

    return updated_user


async def toggle_subscription_to_streams(
        sub_source_names_set: set,
        unsub_source_names_set: set,
        background_tasks: BackgroundTasks,
        user_id: str
):
    for source_name in sub_source_names_set:
        source_schema = available_sources[source_name]()
        background_tasks.add_task(source_schema.subscribe, user_id, source_name)

    for source_name in unsub_source_names_set:
        source_schema = available_sources[source_name]()
        background_tasks.add_task(source_schema.unsubscribe, user_id)
