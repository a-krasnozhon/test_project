from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.deps import get_database, get_auth_user
from app.core.auth import JWTBearer
from app.core.utils import create_access_token
from app.crud.user import CRUDUser
from app.schemas.user import User, UserCreate, UserUpdate, TokenBase

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
        update_data: UserUpdate,
        user: User = Depends(get_auth_user),
        db: AsyncIOMotorClient = Depends(get_database)
):
    updated_user = await CRUDUser(db).update(user, update_data)

    return updated_user
