from typing import Optional, List
from uuid import UUID, uuid4

from beanie import Link
from pydantic import Field, BaseModel

from back_end.models.chat_model import Chat


class FolderOut(BaseModel):
    folder_id: UUID = Field(default_factory=uuid4, alias="folderId")
    name: str
    chat_list: Optional[List[Link[Chat]]] = Field(alias="chatList")


class CreateAndUpdateFolder(BaseModel):
    name: str
    chat_list: set[UUID]
