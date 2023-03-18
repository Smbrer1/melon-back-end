import pymongo.errors
from fastapi import APIRouter, HTTPException, status
from fastapi import Depends

from back_end.api.deps.user_deps import get_current_user
from back_end.models.user_model import User
from back_end.schemas.user_schema import UserAuth, UserOut, UserUpdate
from back_end.services.user_service import UserService

user_router = APIRouter()


@user_router.post("/create", summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    """ Пост для создания юзера

    Args:
        data: Схема аутентификации юзера

    Returns: Схема отправленного юзера

    """
    try:
        return await UserService.create_user(data)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exist",
        )


@user_router.get(
    "/me", summary="Get details of currently logged in user", response_model=UserOut
)
async def get_me(user: User = Depends(get_current_user)):
    """ Гет для получения текущего юзера

    Args:
        user: DI юзера для jwt токена

    Returns: Схема отправленного юзера

    """
    return user


@user_router.post("/update", summary="Update User", response_model=UserOut)
async def update_user(data: UserUpdate, user: User = Depends(get_current_user)):
    """ Пост для обновления юзера

    Args:
        data: Схема обновления юзера
        user: DI юзера для jwt токена

    Returns: Схема отправленного юзера

    """
    try:
        return await UserService.update_user(user.user_id, data)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist"
        )
