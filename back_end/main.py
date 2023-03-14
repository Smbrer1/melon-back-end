from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from back_end.api.api_v1.router import router
from back_end.core.config import settings
from back_end.models.user_model import User

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def app_init():
    """
    initialize crucial application services
    """

    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).melon_back

    await init_beanie(
        database=db_client,
        document_models=[
            User,
        ],
    )


app.include_router(router, prefix=settings.API_V1_STR)
