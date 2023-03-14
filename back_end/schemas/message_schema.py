from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SentMessage(BaseModel):
    text: str
    chat_id: UUID = Field(alias="chatId")
    user_id: UUID = Field(alias="userId")


class MessageOut(BaseModel):
    id: UUID
    chat_id: UUID
    text: str
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]
    is_edited: bool
