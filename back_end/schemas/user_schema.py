from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserAuth(BaseModel):
    phone_number: str = Field(..., alias="phoneNumber", description="phone number")
    username: str = Field(min_length=5, max_length=50, description="username")
    password: str = Field(
        ..., min_length=10, max_length=24, description="user password"
    )


class UserOut(BaseModel):
    user_id: UUID = Field(alias="userId")
    username: str
    phone_number: str = Field(alias="phoneNumber")
    email: Optional[EmailStr]
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")
    disabled: Optional[bool] = False


class UserUpdate(BaseModel):
    phone_number: str = Field(alias="phoneNumber")
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
