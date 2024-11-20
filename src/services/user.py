from fastapi import Depends
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from pydantic import EmailStr

from repositories.user import UserRepository
from schemas.user import UserCreate, UserUpdate
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

    async def update(self, user: User, user_update: UserUpdate):
        user_update_data = user_update.model_dump(exclude_none=True)
        await self.repository.update(user_update_data, user)
