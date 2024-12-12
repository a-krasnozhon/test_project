from fastapi import Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.utils import verify_token
from app.models.user import User
from app.crud.user import CRUDUser


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_database(request: Request):
    return request.app.database


async def get_auth_user(
        db: AsyncIOMotorClient = Depends(get_database),
        token: str = Depends(oauth2_scheme)
) -> User:
    _id = verify_token(token)
    user_data = await CRUDUser(db).get(_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data
