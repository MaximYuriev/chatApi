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


async def get_chat_by_chat_id(
        chat_id: int,
        user: User = Depends(current_user),
        chat_service: ChatService = Depends()
):
    return await chat_service.get_chat(chat_id, user.user_id)


async def recipient_is_bot(
        chat: Annotated[ChatSchema, Depends(get_chat_by_chat_id)],
        user: User = Depends(current_user),
        user_service: UserService = Depends()
):
    if chat.user_2_id == user.user_id:
        return False
    user_2 = await user_service.get_user_by_id(chat.user_2_id)
    return user_2.is_bot
