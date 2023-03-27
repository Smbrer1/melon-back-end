from datetime import datetime
from typing import Optional
from uuid import UUID

import pymongo.errors

from back_end.models.message_model import Message
from back_end.models.user_model import User
from back_end.schemas.generic_response_schema import GenericDelete
from back_end.schemas.message_schema import SentMessage


class MessageService:
    @staticmethod
    async def create_message(message: SentMessage, user: User) -> Optional[Message]:
        """ Создать сообщение

        Args:
            message: Схема сообщения
            user: Схема юзера

        Returns: Модель сообщения

        """
        msg_in = Message(
            chat_id=message.chat_id,
            user_id=user.user_id,
            text=message.text,
        )
        await msg_in.save()
        return msg_in

    @staticmethod
    async def edit_message(msg_id: UUID, text: str, user: User) -> Optional[Message]:
        """ Редактировать сообщение

        Args:
            msg_id: UUID сообщения
            text: Текст сообщения
            user: Модель юзера

        Returns: Модель сообщения

        """
        edited_msg = await Message.find_one(
            Message.msg_id == msg_id, Message.user_id == user.user_id
        )
        if not edited_msg:
            raise pymongo.errors.OperationFailure("Message not found")

        edited_msg.text = text
        edited_msg.updated_at = datetime.now()
        edited_msg.is_edited = True
        await edited_msg.save()
        return edited_msg

    @staticmethod
    async def delete_message(msg_id: UUID, user: User) -> Optional[GenericDelete]:
        """ Удалить сообщение

        Args:
            msg_id: UUID сообщения
            user: Содель юзера

        Returns: Универсальная схема удаления

        """
        deleted_msg = await Message.find_one(
            Message.msg_id == msg_id, Message.user_id == user.user_id
        )
        if not deleted_msg:
            raise pymongo.errors.OperationFailure("Message not found")
        if await deleted_msg.delete():
            return GenericDelete(item={"messageId": msg_id}, success=True)
        else:
            return GenericDelete(item={"messageId": msg_id}, success=False)

    @staticmethod
    async def get_message_by_id(msg_id: UUID, user: User) -> Optional[Message]:
        """ Получить сообщение по UUID

        Args:
            msg_id: UUID сообщения
            user: Модель юзера

        Returns: Модель сообщения

        """
        msg = await Message.find_one(
            Message.msg_id == msg_id, Message.user_id == user.user_id
        )
        return msg
