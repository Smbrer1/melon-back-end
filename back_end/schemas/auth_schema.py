from uuid import UUID

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field

from back_end.schemas.user_schema import UserOut


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    user: UserOut = None
    exp: int = None


class OAuth2TokenScheme(BaseModel):
    phone_number: str = Field(alias="phoneNumber")
    password: str


admin_oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login/",
    scheme_name="OAuth2TokenScheme"
)
