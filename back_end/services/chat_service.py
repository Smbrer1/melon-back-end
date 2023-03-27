from typing import Optional
from uuid import UUID

import pymongo.errors
from beanie.odm.queries.find import FindMany

from back_end.models.chat_model import Chat
from back_end.models.user_model import User
from back_end.schemas.chat_schema import CreateChat, CreateDM, ChatInvitation, GenericChatScheme
from back_end.schemas.generic_response_schema import GenericDelete


class ChatService:
    @staticmethod
    async def create_chat(chat: CreateChat, user: User) -> Optional[Chat]:
        """ Создать чат в бд

        Args:
            chat: Схема создания чата
            user: Модель юзера

        Returns: Модель чата

        """
        chat_in = Chat(
            name=chat.name,
            participants=chat.participants,
            creator_id=user.user_id,
            is_dm=False,
        )
        await chat_in.save()
        return chat_in

    @staticmethod
    async def create_dm(dm: CreateDM, user: User) -> Optional[Chat]:
        """ Создать ЛС в бд

        Args:
            chat: Схема создания ЛС
            user: Модель юзера

        Returns: Модель чата

        """
        dm_in = Chat(name=dm.name, participants={dm.user_id, user.user_id})
        await dm_in.save()
        return dm_in

    @staticmethod
    async def delete_chat(chat_id: UUID, user: User) -> Optional[GenericDelete]:
        """ Удалить чат из бд

        Args:
            chat_id: UUID чата
            user: Модель юзера

        Returns: Универсалья модель удаления

        """
        delete_chat = await Chat.find_one(
            Chat.chat_id == chat_id, Chat.creator_id == user.user_id
        )
        if not delete_chat:
            raise pymongo.errors.OperationFailure("Not allowed or chat not found")
        if await delete_chat.delete():
            return GenericDelete(item={"chatId": delete_chat}, success=True)
        else:
            return GenericDelete(item={"chatId": delete_chat}, success=False)

    @staticmethod
    async def remove_from_chat(chat: GenericChatScheme, user: User) -> Optional[GenericDelete]:
        """ Удалить юзеров из участников чата в бд

        Args:
            chat: Универсальная схема чата
            user: Модель юзера

        Returns: Универсалья модель удаления

        """
        remove_chat = await Chat.find_one(
            Chat.chat_id == chat.chat_id, Chat.creator_id == user.user_id
        )
        if not remove_chat:
            raise pymongo.errors.OperationFailure("Not allowed or chat not found")
        remove_chat.participants.difference(chat.participants)
        if await remove_chat.save():
            return GenericDelete(item={"chatId": remove_chat.chat_id}, success=True)
        else:
            return GenericDelete(item={"chatId": remove_chat.chat_id}, success=False)

    @staticmethod
    async def remove_me_from_chat(chat_id: UUID, user: User) -> Optional[GenericDelete]:
        """ Удаление текущего юзера из чата

        Args:
            chat_id: UUID чата
            user: Модель юзера

        Returns: Универсалья модель удаления

        """
        remove_chat = await Chat.find_one(
            Chat.chat_id == chat_id, user.user_id in Chat.participants
        )
        if not remove_chat:
            raise pymongo.errors.OperationFailure("Chat not found")

        remove_chat.participants.remove(user.user_id)
        if await remove_chat.save():
            return GenericDelete(
                item={"chatId": remove_chat.chat_id, "userId": user.user_id},
                success=True,
            )
        else:
            return GenericDelete(
                item={"chatId": remove_chat.chat_id, "userId": user.user_id},
                success=False,
            )

    @staticmethod
    async def get_chats_by_user_id(user: User) -> Optional[FindMany[Chat]]:
        """ Получение всех чатов юзера

        Args:
            user: Модель юзера

        Returns: Список чатов

        """
        chats = Chat.find_many(user.user_id in Chat.participants)
        if not chats:
            raise pymongo.errors.OperationFailure("User is not in chats")
        return chats

    @staticmethod
    async def invite_to_chat(chat_inv: ChatInvitation, user: User) -> Optional[Chat]:
        """ Приглашение юзеров в чат

        Args:
            chat_inv: Схема приглашения юзеров в чат
            user: Текущий юзер

        Returns: Модель чата

        """
        chat = await Chat.find_one(Chat.chat_id == chat_inv.chat_id, user.user_id in Chat.participants)
        if not chat:
            raise pymongo.errors.OperationFailure("User is not in chats")

        chat.participants.union(chat_inv.participants)
        await chat.save()
        return chat