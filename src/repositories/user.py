from pydantic import EmailStr
from redis import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import User
from schemas.user import Session


class UserRepository:

    @staticmethod
    async def create(session:AsyncSession, data:dict) -> None:
        user = User(**data)
        session.add(user)
        await session.commit()

    @staticmethod
    async def get_user_by_id(session:AsyncSession, user_id:id)->User|None:
        return await session.get(User,user_id)

    @staticmethod
    async def get_user_by_email(session:AsyncSession, email:EmailStr) -> User|None:
        return await session.scalar(select(User).where(User.email == email))

    @staticmethod
    async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
        return await session.scalar(select(User).where(User.username == username))

    @staticmethod
    async def get_user_by_session(session: AsyncSession, user_session:Session) -> User|None:
        return await session.scalar(select(User).where(User.user_id == user_session.user_id))

    @staticmethod
    async def update(session: AsyncSession, user_update: dict, user:User) -> None:
        for key, value in user_update.items():
            setattr(user, key, value)
        await session.commit()

    @staticmethod
    async def get_all_users(session: AsyncSession):
        result = await session.execute(select(User))
        return result.scalars().all()

    # @staticmethod
    # async def get_user_by_param(session:AsyncSession, **kwargs) -> User|None:
    #     return await session.scalar(select(User).filter_by(**kwargs))


class UserRedisRepository:

    @staticmethod
    def set(key: str, value: any, expire: int|None) -> None:
        with Redis() as redis_session:
            redis_session.set(name=key, value=value, ex=expire)

    @staticmethod
    def get(key: str) -> int|None:
        with Redis() as redis_session:
             value = redis_session.get(name = key)
             if value is not None:
                 return int(value)