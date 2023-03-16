from uuid import UUID

from pydantic import BaseModel


class CreateChat(BaseModel):
    name: str
    participants: set[UUID]


class CreateDM(BaseModel):
    name: str
    user_id: UUID


class ChatInvitation(BaseModel):
    chat_id: UUID
    participants: set[UUID]
