from datetime import datetime
from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field

from back_end.utils import get_new_uuid


class ChatRoom(Document):
    chat_id: UUID = Field(default_factory=uuid4, alias="chatId")
    participants: list[UUID]
    creator_id: UUID = Field(alias="creatorId")
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")

    def __repr__(self) -> str:
        return f"<Chat_room {self.id}>"

    @classmethod
    async def by_chat_id(cls, chat_id: str):
        return await cls.find_one(cls.chat_id == chat_id)

    class Settings:
        name = "chat_rooms"
