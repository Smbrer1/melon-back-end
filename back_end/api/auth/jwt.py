from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import ValidationError

from back_end.api.deps.user_deps import get_current_user
from back_end.core.config import settings
from back_end.core.security import create_token
from back_end.models.user_model import User
from back_end.schemas.auth_schema import TokenPayload, admin_oauth2_schema
from back_end.schemas.auth_schema import TokenSchema
from back_end.schemas.user_schema import UserOut
from back_end.services.user_service import UserService

auth_router = APIRouter()


@auth_router.post(
    "/login/",
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema,
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """ Пост для логина юзера

    Args:
        form_data: DI для OAUTH2

    Returns: Словарь с JWT токенами

    """
    user = await UserService.authenticate(
        phone_number=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    return {
        "access_token": create_token(user),
        "refresh_token": create_token(user, is_access=False),
    }


@auth_router.get("/test-token/", summary="Test if the access token is valid", response_model=dict)
async def test_token(user: User = Depends(get_current_user)):
    """ Пост для проверки JWT токена

    Args:
        user: DI юзера для jwt токена

    Returns: Схема для отправленного юзера

    """
    return {
        "access_token": create_token(user),
        "refresh_token": create_token(user),
    }


@auth_router.post("/refresh/", summary="Refresh token", response_model=TokenSchema)
async def refresh_jwt_token(refresh_token: str = Body(...)):
    """ Пост для получения нового токена

    Args:
        refresh_token: refresh токен

    Returns: Схема новых токенов

    """
    try:
        payload = jwt.decode(
            refresh_token,
            settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await UserService.get_user_by_id(token_data.user.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token for user",
        )
    return {
        "access_token": create_token(user),
        "refresh_token": create_token(user),
    }
