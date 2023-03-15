from datetime import datetime
from http.client import HTTPResponse
from typing import Optional
from uuid import UUID

import pymongo.errors
from pymongo.results import DeleteResult

from back_end.models.chat_model import Chat
from back_end.models.message_model import Message
from back_end.models.user_model import User
from back_end.schemas.chat_schema import CreateChat, CreateDM
from back_end.schemas.generic_response_schema import GenericDelete


class MessageService:
    @staticmethod
    async def create_chat(chat: CreateChat) -> Optional[Chat]:
        chat_in = Chat(
            name=chat.name,
            participants=chat.participants,
            is_dm=False
        )
        await chat_in.save()
        return chat_in

    @staticmethod
    async def create_dm(dm: CreateDM) -> Optional[Chat]:
        dm_in = Chat(
            name=dm.name,
            participants=[dm.user_id]
        )
        await dm_in.save()
        return dm_in

    @staticmethod
    async def delete_chat(chat_id: UUID, user: User) -> Optional[GenericDelete]:
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
    async def remove_from_chat(chat_id: UUID, participants: set[UUID], user: User) -> Optional[GenericDelete]:
        remove_chat = await Chat.find_one(
            Chat.chat_id == chat_id, Chat.creator_id == user.user_id
        )
        if not remove_chat:
            raise pymongo.errors.OperationFailure("Not allowed or chat not found")
        remove_chat.participants = remove_chat.participants.difference(participants)
        if await remove_chat.save():
            return GenericDelete(item={"chatId": remove_chat.chat_id}, success=True)
        else:
            return GenericDelete(item={"chatId": remove_chat.chat_id}, success=False)



    @staticmethod
    async def get_message_by_id(msg_id: UUID, user: User) -> Optional[Message]:
        msg = await Message.find_one(
            Message.msg_id == msg_id, Message.user_id == user.user_id
        )
        return msg
