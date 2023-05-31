from asyncio.log import logger

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import Request

from back_end.api.api_v1.router import router
from back_end.core.config import settings
from back_end.models.chat_model import Chat
from back_end.models.message_model import Message
from back_end.models.user_model import User

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_stuff(request: Request, call_next):
    logger.debug(f"{request.method} {request.url}")
    response = await call_next(request)
    logger.debug(response)
    logger.debug(response.status_code)
    return response


@app.on_event("startup")
async def app_init():
    """
    initialize crucial application services
    """

    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).melon_back

    await init_beanie(
        database=db_client,
        document_models=[User, Message, Chat],
    )


app.include_router(router, prefix=settings.API_V1_STR)
