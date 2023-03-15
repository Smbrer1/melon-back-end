from typing import Optional
from uuid import UUID

import pymongo.errors

from back_end.core.security import get_password, verify_password
from back_end.models.user_model import User
from back_end.schemas.user_schema import UserAuth
from back_end.schemas.user_schema import UserUpdate


class UserService:
    @staticmethod
    async def create_user(user: UserAuth):
        user_in = User(
            username=user.username,
            email=user.email,
            hashed_password=get_password(user.password),
        )
        await user_in.save()
        return user_in

    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[User]:
        user = await UserService.get_user_by_email(email=email)
        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.hashed_password):
            return None

        return user

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        user = await User.find_one(User.email == email)
        return user

    @staticmethod
    async def get_user_by_id(uuid: UUID) -> Optional[User]:
        user = await User.find_one(User.user_id == uuid)
        return user

    @staticmethod
    async def update_user(uuid: UUID, data: UserUpdate) -> User:
        user = await User.find_one(User.user_id == uuid)
        if not user:
            raise pymongo.errors.OperationFailure("User not found")
        user.email = data.email
        user.first_name = data.first_name
        user.last_name = data.last_name
        await user.save()
        return user

    # TODO find by username
