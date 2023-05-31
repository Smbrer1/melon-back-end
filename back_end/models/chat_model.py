from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4

from beanie import Document, Link
from pydantic import Field

from back_end.models.user_model import User


class Chat(Document):
    chat_id: UUID = Field(default_factory=uuid4, alias="chatId")
    name: str
    participants: List[Link[User]]
    creator_id: Optional[UUID] = Field(alias="creatorId")
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")
    is_dm: bool = True

    def __repr__(self) -> str:
        return f"<Chat_room {self.id}>"

    class Settings:
        name = "chat_rooms"
