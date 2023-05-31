from datetime import datetime
from encodings.utf_8 import decode
from uuid import uuid4, UUID

from beanie import Document
from pydantic import Field


class Logs(Document):
    log_id: UUID = Field(default_factory=uuid4)
    timestamp: str = Field(default_factory=datetime.now)
    log_value: dict

    def __repr__(self) -> str:
        return f"< {self.id}>"

    class Settings:
        name = "chat_rooms"


async def log_request(req_body, res_body):
    log_in = Logs(
        log_value={"Request": decode(req_body),
                   "Response": decode(res_body)},
    )
    await log_in.save()
