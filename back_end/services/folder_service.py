from typing import Optional
from uuid import UUID

import pymongo.errors
from beanie import WriteRules

from back_end.models.folder_model import Folder
from back_end.models.user_model import User
from back_end.schemas.folder_schemes import CreateAndUpdateFolder


class FolderService:
    @staticmethod
    async def create_folder(folder: CreateAndUpdateFolder, user: User) -> Optional[Folder]:
        """ Создать папку в бд

        Args:
            folder: Схема создания папки
            user: Модель юзера

        Returns: Модель папки

        """
        chats = [await User.find_one(User.user_id == x) for x in folder.chat_list]
        folder_in = Folder(
            name=folder.name,
            chat_list=chats,
            owner=user.user_id,
            is_dm=False,
        )
        await folder_in.save(link_rule=WriteRules.WRITE)
        return folder_in

    @staticmethod
    async def update_folder(uuid: UUID, data: CreateAndUpdateFolder) -> Folder:
        """ Редактировать юзера

        Args:
            uuid: UUID юзера
            data: Схема редактирования юзера

        Returns: Модель юзера

        """
        folder = await Folder.find_one(Folder.owner == uuid)
        if not folder:
            raise pymongo.errors.OperationFailure("User not found")
        folder.chat_list = data.chat_list
        folder.name = data.name
        await folder.save()
        return folder

    @staticmethod
    async def delete_folder(folder_id: UUID, user: User) -> Folder:
        """ Редактировать юзера

        Args:
            user_id: UUID юзера
            folder_id: UUID папки

        Returns: Модель юзера

        """
        delete_folder = await Folder.find_one(
            Folder.folder_id == folder_id, Folder.owner == user
        )
        if not delete_folder:
            raise pymongo.errors.OperationFailure("Not allowed or chat not found")
        if await delete_folder.delete():
            return GenericDelete(item={"chatId": delete_folder}, success=True)
        else:
            return GenericDelete(item={"chatId": delete_folder}, success=False)
