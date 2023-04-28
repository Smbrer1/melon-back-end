from typing import Optional
from uuid import UUID

import pymongo.errors
from beanie.odm.queries.find import FindMany

from back_end.models.chat_model import Chat
from back_end.models.user_model import User
from back_end.schemas.chat_schema import CreateChat, CreateDM, ChatInvitation, GenericChatScheme
from back_end.schemas.generic_response_schema import GenericDelete


class FriendService:
    @staticmethod
    async def send_friend_request( user: User) -> Optional[Chat]:
        """ Создать чат в бд

        Args:
            --------needs to be changed----------
            chat: Схема создания чата
            user: Модель юзера

        Returns: Модель чата

        """
        friend_in = Chat(
            user_id=user.user_id,
            friend_id=user.user_id,
            is_dm=False,
        )
        await friend_in.save()
        return friend_in

    @staticmethod
    async def accept_friend_request(user: User ,accpet: bool ,friend_id: UUID) -> Optional[Chat]:
        """ Создать чат в бд

        Args:
            --------needs to be changed----------
            chat: Схема создания чата
            user: Модель юзера

        Returns: Модель чата

        """
        friend_in = Chat(
            user_id=user.user_id,
            friend_id=friend_id,
            is_friend=accpet,
        )
        if friend_in.is_friend:
            if await user.save():
                return GenericDelete(item={"friend_list": user.friend_id}, success=True)
        else:
            return GenericDelete(item={"friend_list": user.friend_id}, success=False)


        if not friend_in:
            raise pymongo.errors.OperationFailure("User not found")
        user.friend_list.difference(remove_friend)
        if await user.save():
            return GenericDelete(item={"friend_list": remove_friend.friend_id}, success=True)
        else:
            return GenericDelete(item={"friend_list": remove_friend.friend_id}, success=False)
    @staticmethod
    async def remove_from_friendlist(chat: GenericChatScheme, user: User, friend_id: UUID) -> Optional[GenericDelete]:
        """ Удалить юзеров из участников чата в бд

        Args:
             --------needs to be changed----------
            chat: Универсальная схема чата
            user: Модель юзера

        Returns: Универсалья модель удаления

        """
        remove_friend = await User.find_one(
            User.user_id == friend_id
        )
        if not remove_friend:
            raise pymongo.errors.OperationFailure("User not found")
        user.friend_list.difference(remove_friend)
        if await user.save():
            return GenericDelete(item={"friend_list": remove_friend.friend_id}, success=True)
        else:
            return GenericDelete(item={"friend_list": remove_friend.friend_id}, success=False)
