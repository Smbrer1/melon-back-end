from datetime import datetime
from http.client import HTTPResponse
from typing import Optional
from uuid import UUID

import pymongo.errors
from pymongo.results import DeleteResult

from back_end.models.message_model import Message
from back_end.models.user_model import User
from back_end.schemas.generic_response_schema import GenericDelete
from back_end.schemas.message_schema import SentMessage, MessageDelete, DeletedMessage


class MessageService:
    @staticmethod
    async def create_message(message: SentMessage, user: User):
        msg_in = Message(
            chat_id=message.chat_id,
            user_id=user.user_id,
            text=message.text,
        )
        await msg_in.save()
        return msg_in

    @staticmethod
    async def edit_message(msg_id: UUID, text: str, user: User) -> Optional[Message]:
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
    async def delete_message(msg: MessageDelete, user: User) -> Optional[GenericDelete]:
        deleted_msg = await Message.find_one(
            Message.msg_id == msg.msg_id, Message.user_id == user.user_id
        )
        if not deleted_msg:
            raise pymongo.errors.OperationFailure("Message not found")
        if await deleted_msg.delete():
            return GenericDelete(item={"messageId": msg.msg_id}, success=True)
        else:
            return GenericDelete(item={"messageId": msg.msg_id}, success=False)


    @staticmethod
    async def get_message_by_id(msg_id: UUID, user: User) -> Optional[Message]:
        msg = await Message.find_one(
            Message.msg_id == msg_id, Message.user_id == user.user_id
        )
        return msg
