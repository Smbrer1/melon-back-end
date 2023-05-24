from typing import Optional, List
from uuid import UUID

from beanie import Link
from pydantic import BaseModel, Field

from back_end.models.user_model import User


class GenericChatScheme(BaseModel):
    chat_id: Optional[UUID] = Field(alias="chatId")
    participants: List[Link[User]]


class CreatedChat(BaseModel):
    name: str
    chat_id: UUID = Field(alias="chatId")
    participants: List[Link[User]]


class CreateChat(BaseModel):
    name: str
    participants: set[UUID]


class CreateDM(BaseModel):
    name: str
    user_id: UUID = Field(alias="userId")


class ChatInvitation(BaseModel):
    chat_id: UUID = Field(alias="chatId")
    participants: List[Link[User]]
