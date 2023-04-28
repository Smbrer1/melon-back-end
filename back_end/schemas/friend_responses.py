from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class FriendsAddOut(BaseModel):
    user_sender: UUID = Field(alias="userSender")
    user_reciever: UUID = Field(alias="userReciever")
    success: bool
