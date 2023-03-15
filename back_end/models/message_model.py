from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import Field

from back_end.utils import get_new_uuid


class Message(Document):
    msg_id: UUID = Field(default_factory=uuid4, alias="msgId")
    chat_id: Indexed(UUID) = Field(alias="chatId")
    text: str
    user_id: UUID = Field(alias="userId")
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")
    updated_at: Optional[datetime] = Field(alias="updatedAt")
    is_edited: bool = Field(default=False, alias="isEdited")

    def __repr__(self) -> str:
        return f"<Message {self.id}>"

    def __str__(self) -> str:
        return self.text

    @classmethod
    def by_chat_id(cls, chat_id: str):
        return cls.find_many(cls.chat_id == chat_id)

    class Settings:
        name = "messages"
