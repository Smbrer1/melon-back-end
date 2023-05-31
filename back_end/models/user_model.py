from typing import Optional
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import Field, EmailStr, constr


class User(Document):
    user_id: UUID = Field(default_factory=uuid4, alias="userId")
    username: Indexed(str, unique=True)
    phone_number: Indexed(constr(max_length=50, strip_whitespace=True)) = Field(alias="phoneNumber")
    email: Optional[EmailStr]
    hashed_password: str = Field(alias="hashedPassword")
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")
    disabled: Optional[bool] = False

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __str__(self) -> str:
        return self.email

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.email == other.email
        return False

    class Settings:
        name = "users"
