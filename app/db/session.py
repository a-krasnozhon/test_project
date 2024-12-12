from pymongo import AsyncMongoClient

from app.core.config import settings

db = AsyncMongoClient(settings.MONGO_CONNECTION_URI)
