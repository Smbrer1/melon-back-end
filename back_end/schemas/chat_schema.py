from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CreateChat(BaseModel):
    name: str
    participants: set[UUID]


class CreateDM(BaseModel):
    name: str
    user_id: UUID
