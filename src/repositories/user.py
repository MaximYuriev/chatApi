from fastapi import Depends
from redis import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_session
from models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create(self, user_data: dict) -> None:
        user = User(**user_data)
        self.session.add(user)
        await self.session.commit()

    async def get_user_by_id(self, user_id: id) -> User | None:
        return await self.session.get(User, user_id)

    async def get_user_by_param(self, **kwargs) -> User | None:
        return await self.session.scalar(select(User).filter_by(**kwargs))

    async def update(self, user_update: dict, user: User) -> None:
        for key, value in user_update.items():
            setattr(user, key, value)
        await self.session.commit()

    async def get_all_users(self):
        result = await self.session.execute(select(User))
        return result.scalars().all()


class UserRedisRepository:

    @staticmethod
    def set(key: str, value: any, expire: int | None) -> None:
        with Redis() as redis_session:
            redis_session.set(name=key, value=value, ex=expire)

    @staticmethod
    def get(key: str) -> int | None:
        with Redis() as redis_session:
            value = redis_session.get(name=key)
            if value is not None:
                return int(value)
