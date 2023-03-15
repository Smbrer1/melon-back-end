from datetime import datetime
from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field


class Chat(Document):
    chat_id: UUID = Field(default_factory=uuid4, alias="chatId")
    participants: set[UUID]
    creator_id: UUID = Field(alias="creatorId")
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")
    is_dm: bool = True

    def __repr__(self) -> str:
        return f"<Chat_room {self.id}>"

    class Settings:
        name = "chat_rooms"
