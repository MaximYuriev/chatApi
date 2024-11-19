from fastapi import Depends
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from pydantic import EmailStr

from repositories.user import UserRepository
from schemas.user import UserCreate
from models.user import User


class UserService:
    def __init__(self, repository: UserRepository = Depends()):
        self.repository = repository

    async def create(self, user: UserCreate):
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
