from uuid import UUID

import pymongo.errors
from fastapi import APIRouter, HTTPException, status
from fastapi import Depends

from back_end.api.deps.user_deps import get_current_user
from back_end.models.folder_model import Folder
from back_end.models.user_model import User
from back_end.schemas.folder_schemes import FolderOut, CreateAndUpdateFolder
from back_end.schemas.user_schema import UserAuth, UserOut, UserUpdate
from back_end.services.folder_service import FolderService
from back_end.services.user_service import UserService

folder_router = APIRouter()


@folder_router.post("/create/", summary="Create new folder", response_model=FolderOut)
async def create_folder(data: CreateAndUpdateFolder, user: User = Depends(get_current_user)):
    """ Пост для создания юзера

    Args:
        user: DI юзера для jwt токена
        data: Схема создания папки

    Returns: Схема отправленной папки

    """
    try:
        return await FolderService.create_folder(data, user)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create folder",
        )


@folder_router.post("/update/", summary="Update existing folder", response_model=FolderOut)
async def update_folder(data: CreateAndUpdateFolder, user: User = Depends(get_current_user)):
    """ Пост для апдейта папки

    Args:
        user: DI юзера для jwt токена
        data: Схема обновления папки

    Returns: Схема отправленной папки

    """
    try:
        return await FolderService.create_folder(data, user)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create folder",
        )


@folder_router.post("/delete/", summary="Delete Folder", response_model=UserOut)
async def update_user(folder_id: UUID, user: User = Depends(get_current_user)):
    """ Пост для обновления юзера

    Args:
        folder_id: UUID папки
        user: DI юзера для jwt токена

    Returns: Схема отправленного юзера

    """
    try:
        return await FolderService.delete_folder(folder_id, user.user_id)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Folder does not exists"
        )
