import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import Session


class SessionRepository:

    @staticmethod
    async def create(session:AsyncSession, add_session_data:dict) -> uuid.UUID:
        user_session = Session(**add_session_data)
        session.add(user_session)
        await session.commit()
        return user_session.session_id

    @staticmethod
    async def get_session_by_id(session:AsyncSession, session_id: uuid.UUID) -> Session|None:
        return await session.get(Session, session_id)

    @staticmethod
    async def delete(session: AsyncSession, user_session:Session) -> None:
        await session.delete(user_session)
        await session.commit()