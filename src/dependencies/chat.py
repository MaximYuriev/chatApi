from typing import Annotated

from fastapi import Depends

from dependencies.auth import current_user
from exceptions.chat import ChatAlreadyExist
from exceptions.user import UserNotFound
from models.user import User
from schemas.chat import ChatCreate, ChatSchema
from services.chat import ChatService
from services.user import UserService


async def validate_chat_create(
        chat: ChatCreate,
        user: Annotated[User, Depends(current_user)],
        user_service: UserService = Depends(),
        chat_service: ChatService = Depends()
):
    user_2 = await user_service.get_user_by_username(chat.username)
    if user_2 is None:
        raise UserNotFound

    if await chat_service.get_chat_between_users(user_1_id=user.user_id, user_2_id=user_2.user_id):
        raise ChatAlreadyExist

    return ChatSchema(user_1_id=user.user_id, user_2_id=user_2.user_id)
