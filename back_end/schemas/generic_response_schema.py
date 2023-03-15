from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class GenericDelete(BaseModel):
    item: dict = Field(default={"itemName": "itemValue"})
    success: bool
