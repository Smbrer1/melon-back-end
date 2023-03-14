from typing import Optional
from uuid import UUID

import pymongo.errors

from back_end.models.message_model import Message
from back_end.schemas.message_schema import SentMessage


class MessageService:
    @staticmethod
    async def create_message(message: SentMessage):
        message_in = Message(
            chat_id=SentMessage.chat_id,
            user_id=message.user_id,
            text=message.text,
        )
        await message_in.save()
        return message_in

    @staticmethod
    async def edit_message(uuid: UUID, text: str) -> Optional[Message]:
        edited_message = await Message.find_one(Message.id == uuid)
        if not edited_message:
            raise pymongo.errors.OperationFailure("Message not found")

        await edited_message.update({"$set": {"text": text}})
        return edited_message

    @staticmethod
    async def get_message_by_id(uuid: UUID) -> Optional[Message]:
        user = await Message.find_one(Message.id == uuid)
        return user
