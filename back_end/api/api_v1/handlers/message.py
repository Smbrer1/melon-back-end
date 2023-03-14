from uuid import UUID

import pymongo.errors
from fastapi import APIRouter, HTTPException, status

from back_end.schemas.message_schema import SentMessage, MessageOut
from back_end.services.message_service import MessageService

message_router = APIRouter()


@message_router.post("/send", summary="Send new message", response_model=MessageOut)
async def send_message(data: SentMessage):
    try:
        return await MessageService.create_message(data)
    except pymongo.errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid message",
        )


@message_router.post("/edit", summary="Edit message", response_model=MessageOut)
async def edit_message(message_id: UUID, text: str):
    try:
        return await MessageService.edit_message(message_id, text)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Message does not exist"
        )
