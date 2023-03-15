from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SentMessage(BaseModel):
    text: str
    chat_id: UUID = Field(alias="chatId")


class MessageDelete(BaseModel):
    msg_id: UUID = Field(alias="msgId")


class MessageOut(BaseModel):
    msg_id: UUID = Field(alias="msgId")
    chat_id: UUID = Field(alias="chatId")
    text: str
    user_id: UUID = Field(alias="userId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: Optional[datetime] = Field(alias="updatedAt")
    is_edited: bool = Field(alias="isEdited")


class DeletedMessage(BaseModel):
    msg_id: UUID = Field(alias="msgId")
    success: bool

