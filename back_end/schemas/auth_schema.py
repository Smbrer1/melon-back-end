from uuid import UUID

from pydantic import BaseModel

from back_end.schemas.user_schema import UserOut


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    user: UserOut = None
    exp: int = None
