from fastapi import HTTPException, Response, Depends
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from config import COOKIES_KEY_NAME
from schemas.session import UserSession
from repositories.user import UserRepository
from schemas.user import UserCreate
from models.user import Session, User
from services.session import SessionService
from bgtask.task import send_email_message
from services.user_redis import UserRedisService


class UserService:
    def __init__(self, repository: UserRepository = Depends()):
        self.repository = repository

    async def create(self, user:UserCreate):
        user.password = pbkdf2_sha256.hash(user.password)
        add_user_data = user.model_dump(exclude_unset=True)
        await self.repository.create(add_user_data)
        return {"detail": "Пользователь зарегистрирован", "data": None}

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.repository.get_user_by_id(user_id)

    async def get_user_by_email(self, email: EmailStr | str) -> User | None:
        return await self.repository.get_user_by_param(email=email)

    async def get_user_by_username(self, username: str) -> User | None:
        return await self.repository.get_user_by_param(username=username)

    # async def get_user_by_session(self, user_session: Session) -> User | None:
    #     user = await self.repository.get_user_by_session(user_session)
    #     if user is None:
    #         raise HTTPException(status_code=403, detail="Нет доступа")
    #     return user
    #
    # async def login(self, user_auth:UserLogin, user_agent: str|None = None,
    #                 cookies: str|None = None):
    #     if cookies is not None:
    #         raise HTTPException(status_code=400, detail="Вход уже выполнен")
    #
    #
    #     user_session = UserSession(user_id=user.user_id, user_agent=user_agent)
    #     session_id = await SessionService.create(session, user_session)
    #
    #     response.set_cookie(key=COOKIES_KEY_NAME, value=session_id, httponly=True)
    #     return {"detail": "Пользователь вошел в аккаунт", "data": None}
    #
    # @staticmethod
    # async def logout(session: AsyncSession, response:Response, user_session:Session):
    #     await SessionService.delete(session, user_session)
    #     response.delete_cookie(COOKIES_KEY_NAME)
    #     return {"detail":"Пользователь вышел!", "data":None}
    #
    # @staticmethod
    # def send_verify_code(user:User):
    #     if user.is_verify:
    #         raise HTTPException(status_code=400, detail="Аккаунт уже верифицирован")
    #     send_email_message.delay(user.email, user.user_id)
    #     return {"detail": f"Письмо отправлено на почту {user.email}", "data": None}
    #
    # @staticmethod
    # async def verify_account(session: AsyncSession, user:User, user_code: int):
    #     if user.is_verify:
    #         raise HTTPException(status_code=400, detail="Аккаунт уже верифицирован!")
    #
    #     UserRedisService.check_verify_code(user.user_id, user_code)
    #
    #     user_update = UserUpdate(is_verify=True).model_dump(exclude_unset=True)
    #     await UserRepository.update(session, user_update, user)
    #     return {"detail":"Аккаунт успешно верифицирован!", "data":None}
    #
    # @staticmethod
    # async def get_all_users(session: AsyncSession):
    #     all_users_orm = await UserRepository.get_all_users(session)
    #     all_users = [UserRead.model_validate(user, from_attributes=True) for user in all_users_orm]
    #     return all_users
