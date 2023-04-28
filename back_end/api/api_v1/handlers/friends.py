from uuid import UUID

import pymongo.errors
from fastapi import APIRouter, HTTPException, status, Depends

from back_end.api.deps.user_deps import get_current_user
from back_end.schemas.chat_schema import CreateChat, ChatInvitation, CreateDM, GenericChatScheme
from back_end.schemas.generic_response_schema import GenericDelete
from back_end.services.chat_service import ChatService

friends_router = APIRouter()
@friends_router.post("/add", summary="add new friend", response_model=)
async def send_message(data: SentMessage, user=Depends(get_current_user)):
    """ Пост для отправления сообщений

    Args:
        data: Схема отправленного сообщения
        user: DI юзера для jwt токена

    Returns: Схема отправленного сообщения

    """
    return await MessageService.create_message(data, user)


@friends_router.post("/edit", summary="Edit message", response_model=MessageOut)
async def edit_message(message_id: UUID, text: str, user=Depends(get_current_user)):
    """ Пост для редактирования сообщения

    Args:
        message_id: UUID сообщения
        text: Текст сообщения
        user: DI юзера для jwt токена

    Returns: Схема отправленного сообщения

    """
    try:
        return await MessageService.edit_message(message_id, text, user)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Message does not exist"
        )


@friends_router.post("/delete", summary="Delete message", response_model=GenericDelete)
async def delete_message(message_id: UUID, user=Depends(get_current_user)):
    """ Пост для удаления сообщений

    Args:
        message_id: UUID
        user: Схема отправленного сообщения

    Returns: Универсальная схема удаления

    """
    try:
        return await MessageService.delete_message(message_id, user)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Message does not exist"
        )
