from fastapi import APIRouter

from app.api.api_v1.endpoints import user, source

api_router = APIRouter(redirect_slashes=True)

api_router.include_router(user.router, prefix='/user', tags=['user'])
api_router.include_router(source.router, prefix='/source', tags=['source'])
