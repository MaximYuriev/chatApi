from typing import Annotated

from fastapi import Depends, Body

from dependencies.auth import current_user
from exceptions.user import UserAlreadyVerify, InvalidCodeError, CodeIsNotCorrect
from models.user import User
from services.user_redis import UserRedisService


async def check_verify_user(
        user: Annotated[User, Depends(current_user)]
):
    if user.is_verify:
        raise UserAlreadyVerify
    return user


def create_message_data(
        user: Annotated[User, Depends(check_verify_user)]
):
    code_value = UserRedisService.generation_verify_code(user.user_id)
    return {"email": user.email, "code_value": code_value}


def validate_verify_code(
        verify_code: Annotated[int, Body()],
        user: Annotated[User, Depends(check_verify_user)]
):
    true_code = UserRedisService.get(user_id=user.user_id)
    if true_code is None:
        raise InvalidCodeError
    if verify_code != true_code:
        raise CodeIsNotCorrect
