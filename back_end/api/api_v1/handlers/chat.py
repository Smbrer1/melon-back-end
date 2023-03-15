from uuid import UUID

import pymongo.errors
from fastapi import APIRouter, HTTPException, status, Depends

from back_end.api.deps.user_deps import get_current_user
from back_end.schemas.chat_schema import CreateChat
from back_end.schemas.generic_response_schema import GenericDelete
from back_end.schemas.message_schema import SentMessage, MessageOut
from back_end.services.message_service import MessageService

chat_router = APIRouter()


@chat_router.post("/create", summary="Send new message", response_model=MessageOut)
async def create_chat(data: CreateChat, user=Depends(get_current_user)):
    return await ChatService.create_chat(data, user)


@chat_router.post("/invite", summary="Edit message", response_model=MessageOut)
async def invite_to_chat(message_id: UUID, text: str, user=Depends(get_current_user)):
    try:
        return await MessageService.edit_message(message_id, text, user)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Message does not exist"
        )


@chat_router.post("/delete", summary="Delete message", response_model=GenericDelete)
async def delete_chat(msg: MessageDelete, user=Depends(get_current_user)):
    try:
        return await MessageService.delete_message(msg, user)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Message does not exist"
        )
