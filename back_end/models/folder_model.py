from typing import List, Optional
from uuid import UUID, uuid4

from beanie import Document, Link
from pydantic import Field

from back_end.models.chat_model import Chat
from back_end.models.user_model import User


class Folder(Document):
    folder_id: UUID = Field(default_factory=uuid4, alias="folderId")
    name: str
    owner: Link[User]
    chat_list: Optional[List[Link[Chat]]] = Field(alias="chatList")

    class Settings:
        name = "folders"
