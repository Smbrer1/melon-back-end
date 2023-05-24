from typing import Optional, Union
from uuid import UUID, uuid4

from beanie import Document, Indexed
from phonenumbers import (
    NumberParseException,
    PhoneNumberFormat,
    PhoneNumberType,
    format_number,
    is_valid_number,
    number_type,
    parse as parse_phone_number,
)
from pydantic import Field, EmailStr, constr, validator

MOBILE_NUMBER_TYPES = PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE


class User(Document):
    user_id: UUID = Field(default_factory=uuid4, alias="userId")
    username: Indexed(str, unique=True)
    phone_number: constr(max_length=50, strip_whitespace=True) = None
    email: Indexed(EmailStr, unique=True)
    hashed_password: str = Field(alias="hashedPassword")
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")
    disabled: Optional[bool] = False

    @validator('phone_number')
    def check_phone_number(cls, phone) -> Optional[str]:
        if phone is None:
            return phone

        try:
            parsed_phone = parse_phone_number(phone, 'RU')
        except NumberParseException as e:
            raise ValueError('Please provide a valid mobile phone number') from e

        if not is_valid_number(parsed_phone) or number_type(parsed_phone) not in MOBILE_NUMBER_TYPES:
            raise ValueError('Please provide a valid mobile phone number')

        return format_number(
            parsed_phone,
            PhoneNumberFormat.NATIONAL if parsed_phone.country_code == 7 else PhoneNumberFormat.INTERNATIONAL
        )

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
