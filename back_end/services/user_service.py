from typing import Optional
from uuid import UUID

import pymongo.errors
from beanie.odm.queries.find import FindMany

from back_end.core.security import get_password, verify_password
from back_end.models.user_model import User
from back_end.schemas.user_schema import UserAuth
from back_end.schemas.user_schema import UserUpdate


class UserService:
    @staticmethod
    async def create_user(user: UserAuth) -> Optional[User]:
        """ Создать юзера в бд

        Args:
            user: Модель авторизации юзера

        Returns: Модель юзера

        """
        user_in = User(
            username=user.username,
            email=user.email,
            hashed_password=get_password(user.password),
        )
        await user_in.save()
        return user_in

    @staticmethod
    async def authenticate(phone_number: str, password: str) -> Optional[User]:
        """ Аутентификация юзера

        Args:
            email: Почта пользователя
            password: Пароль пользователя

        Returns: Модель юзера

        """
        user = await UserService.get_user_by_email(phone=phone_number)
        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.hashed_password):
            return None

        return user

    @staticmethod
    async def get_user_by_phone_number(phone_number: str) -> Optional[User]:
        """ Получить юзера по номеру телефона

        Args:
            phone_number: номер телефона

        Returns: Модель юзера

        """
        user = await User.find_one(User.phone_number == phone_number)
        return user

    @staticmethod
    async def get_user_by_id(uuid: UUID) -> Optional[User]:
        """ Получить юзера по ID

        Args:
            uuid: UUID юзера

        Returns: Модель юзера

        """
        user = await User.find_one(User.user_id == uuid)
        return user

    @staticmethod
    async def update_user(uuid: UUID, data: UserUpdate) -> User:
        """ Редактировать юзера

        Args:
            uuid: UUID юзера
            data: Схема редактирования юзера

        Returns: Модель юзера

        """
        user = await User.find_one(User.user_id == uuid)
        if not user:
            raise pymongo.errors.OperationFailure("User not found")
        user.phone_number = data.phone_number
        user.first_name = data.first_name
        user.last_name = data.last_name
        await user.save()
        return user

    @staticmethod
    async def find_like_username(username: str) -> Optional[FindMany[User]]:
        return User.find_many({"username": f"/^{username}/"})
