from fastapi import HTTPException, Response
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy.ext.asyncio import AsyncSession

from config import COOKIES_KEY_NAME
from src.models.session import UserSession
from repositories.user import UserRepository
from src.models.user import User as UserSchemas, UserLogin, UserUpdate, UserRead
from schemas.user import Session, User
from services.session import SessionService
from src.bgtask.task import send_email_message
from services.user_redis import UserRedisService


class UserService:

    @staticmethod
    async def create(session:AsyncSession, user:UserSchemas):
        if await UserRepository.get_user_by_email(session, user.email):
            raise HTTPException(status_code=400, detail="Данная почта зарегистрирована в системе!")
        if await UserRepository.get_user_by_username(session, user.username):
            raise HTTPException(status_code=400, detail="Имя пользователя занято!")

        user.password = pbkdf2_sha256.hash(user.password)

        add_user_data = user.model_dump(exclude_unset=True)
        await UserRepository.create(session, add_user_data)
        return {"detail": "Пользователь зарегистрирован", "data": None}

    @staticmethod
    async def get_user_by_session(session: AsyncSession, user_session: Session):
        user = await UserRepository.get_user_by_session(session, user_session)
        if user is None:
            raise HTTPException(status_code=403, detail="Нет доступа")
        return user

    @staticmethod
    async def login(session:AsyncSession, response:Response, user_auth:UserLogin, user_agent: str|None = None,
                    cookies: str|None = None):
        if cookies is not None:
            raise HTTPException(status_code=400, detail="Вход уже выполнен")
        user = await UserRepository.get_user_by_email(session, user_auth.email)
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь с данной почтой не найден!")

        if not pbkdf2_sha256.verify(user_auth.password, user.password):
            raise HTTPException(status_code=403, detail="Неверный пароль!")

        user_session = UserSession(user_id=user.user_id, user_agent=user_agent)
        session_id = await SessionService.create(session, user_session)

        response.set_cookie(key=COOKIES_KEY_NAME, value=session_id, httponly=True)
        return {"detail": "Пользователь вошел в аккаунт", "data": None}

    @staticmethod
    async def logout(session: AsyncSession, response:Response, user_session:Session):
        await SessionService.delete(session, user_session)
        response.delete_cookie(COOKIES_KEY_NAME)
        return {"detail":"Пользователь вышел!", "data":None}

    @staticmethod
    def send_verify_code(user:User):
        if user.is_verify:
            raise HTTPException(status_code=400, detail="Аккаунт уже верифицирован")
        send_email_message.delay(user.email, user.user_id)
        return {"detail": f"Письмо отправлено на почту {user.email}", "data": None}

    @staticmethod
    async def verify_account(session: AsyncSession, user:User, user_code: int):
        if user.is_verify:
            raise HTTPException(status_code=400, detail="Аккаунт уже верифицирован!")

        UserRedisService.check_verify_code(user.user_id, user_code)

        user_update = UserUpdate(is_verify=True).model_dump(exclude_unset=True)
        await UserRepository.update(session, user_update, user)
        return {"detail":"Аккаунт успешно верифицирован!", "data":None}

    @staticmethod
    async def get_all_users(session: AsyncSession):
        all_users_orm = await UserRepository.get_all_users(session)
        all_users = [UserRead.model_validate(user, from_attributes=True) for user in all_users_orm]
        return all_users
