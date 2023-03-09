from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

from models.user_model import User

from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
load_dotenv()
melon = FastAPI()
config_dict = os.environ
session = {}


@melon.get("/")
async def root() -> dict:
    return {"message": config_dict.get("DB_LINK")}


@melon.post("/authorize/")
async def authorize(user: User, token: str = Depends(oauth2_scheme)) -> dict:
    """Пост запрос с авторизацией юзера

    Args:
        user: Схема юзера
        token: токен регистрации

    Returns: Ответ на запрос

    """
    session["username"] = user.username
    session["password"] = user.password
    return {"message": "ok", "token": token}


@melon.get("/authorize/")
async def get_credentials() -> dict:
    return session
