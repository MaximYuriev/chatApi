from typing import Annotated

from fastapi import APIRouter, Depends

from dependencies.auth import validate_reg_user, prepare_user_session, current_session
from schemas.session import UserSession
from services.session import SessionService
from models.user import Session
from schemas.user import UserCreate
from services.user import UserService

auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.post('/registration')
async def user_registration(
        user_create: Annotated[UserCreate, Depends(validate_reg_user)],
        user_service: UserService = Depends()
):
    return await user_service.create(user_create)


@auth_router.post('/login')
async def user_login(
        user_session: UserSession = Depends(prepare_user_session),
        session_service: SessionService = Depends()
):
    await session_service.create(user_session)
    return {"detail": "Пользователь авторизован!", "data": None}


@auth_router.get('/logout')
async def user_logout(
        user_session: Annotated[Session, Depends(current_session)],
        session_service: SessionService = Depends()
):
    await session_service.delete_with_cookie(user_session)
    return {"detail": "Пользователь вышел!", "data": None}
