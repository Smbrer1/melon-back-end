from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class GenericChatScheme(BaseModel):
    chat_id: Optional[UUID] = Field(alias="chatId")
    participants: set[UUID]


class CreatedChat(BaseModel):
    name: str
    chat_id: UUID = Field(alias="chatId")
    participants: set[UUID]


class CreateChat(BaseModel):
    name: str
    participants: set[UUID]


class CreateDM(BaseModel):
    name: str
    user_id: UUID = Field(alias="userId")


class ChatInvitation(BaseModel):
    chat_id: UUID = Field(alias="chatId")
    participants: set[UUID]
