import logging
from logging import INFO

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.api_v1.api import api_router
from app.core.config import settings


logging.getLogger('root').setLevel('INFO')
logging.lastResort.setLevel(INFO)

app = FastAPI(
    title='test_project',
    description='',
    version='1.0.0',
    openapi_url=settings.OPENAPI_URL,
)

# CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_URI)
    app.database = app.mongodb_client.get_default_database(default='default')

    ping_response = await app.database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")


@app.on_event("shutdown")
async def shutdown_db_client():
    print("Closing MongoDB connection.")
    app.mongodb_client.close()


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
