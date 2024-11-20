from typing import Annotated

from fastapi import Depends, Header
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from models.user import Session
from schemas.session import UserSession
from schemas.user import UserCreate, UserLogin
from services.session import SessionService
from services.user import UserService
from exceptions.auth import EmailAlreadyExist, UsernameAlreadyExist, EmailNotFound, InvalidPassword, NotAuthorized


async def validate_reg_user(user_create: UserCreate, user_service: UserService = Depends()):
    if await user_service.get_user_by_email(user_create.email):
        raise EmailAlreadyExist
    if await user_service.get_user_by_username(user_create.username):
        raise UsernameAlreadyExist
    return user_create


async def validate_auth_user(user_auth: UserLogin, user_service: UserService = Depends()):
    user = await user_service.get_user_by_email(user_auth.email)
    if user is None:
        raise EmailNotFound

    if not pbkdf2_sha256.verify(user_auth.password, user.password):
        raise InvalidPassword

    return user.user_id


async def prepare_user_session(
        user_id: Annotated[int, Depends(validate_auth_user)],
        user_agent: Annotated[str | None, Header()] = None
):
    return UserSession(user_id=user_id, user_agent=user_agent)


def validate_cookie(session_service: SessionService = Depends()):
    cookies = session_service.get_cookie()
    if cookies is None:
        raise NotAuthorized
    return cookies


async def current_session(
        cookies: Annotated[Session, Depends(validate_cookie)],
        session_service: SessionService = Depends()
):
    session = await session_service.get_session(cookies)
    return session


async def current_user(
        session: Annotated[Session, Depends(current_session)],
        user_service: UserService = Depends()
):
    return await user_service.get_user_by_id(session.user_id)
