from datetime import datetime
from encodings.utf_8 import decode

from beanie import Document
from pydantic import Field


class Logs(Document):
    timestamp: datetime = Field(default_factory=datetime.now)
    log_value: dict

    def __repr__(self) -> str:
        return f"< {self.id}>"

    class Settings:
        name = "logs"


async def log_request(req_body, res_body):
    log_in = Logs(
        log_value={"Request": decode(req_body),
                   "Response": decode(res_body)},
    )
    print(log_in.json())
    await log_in.save()
    return log_in
