import pymongo.errors
from fastapi import APIRouter, HTTPException, status, Depends

from back_end.api.deps.user_deps import get_current_user
from back_end.services.chat_service import ChatService

friends_router = APIRouter()


@friends_router.get("/me", summary="Find all user chats")
def get_my_chats(user: Depends(get_current_user)):
    """Пост для удаления текущего юзера из чата

    Args:
        user: DI юзера для jwt токена

    Returns: Универсальная схема удаления

    """
    try:
        return await ChatService.get_chats_by_user_id(user.user_id)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist"
        )
