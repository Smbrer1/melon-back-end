from uuid import UUID

from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")


class TokenPayload(BaseModel):
    sub: UUID = None
    exp: int = None
