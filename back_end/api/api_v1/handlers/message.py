from uuid import UUID

import pymongo.errors
from fastapi import APIRouter, HTTPException, status, Depends

from back_end.api.deps.user_deps import get_current_user
from back_end.schemas.generic_response_schema import GenericDelete
from back_end.schemas.message_schema import SentMessage, MessageOut
from back_end.services.message_service import MessageService

message_router = APIRouter()


@message_router.post("/send", summary="Send new message", response_model=MessageOut)
async def send_message(data: SentMessage, user=Depends(get_current_user)):
    return await MessageService.create_message(data, user)


@message_router.post("/edit", summary="Edit message", response_model=MessageOut)
async def edit_message(message_id: UUID, text: str, user=Depends(get_current_user)):
    try:
        return await MessageService.edit_message(message_id, text, user)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Message does not exist"
        )


@message_router.post("/delete", summary="Delete message", response_model=GenericDelete)
async def delete_message(message_id: UUID, user=Depends(get_current_user)):
    try:
        return await MessageService.delete_message(message_id, user)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Message does not exist"
        )
