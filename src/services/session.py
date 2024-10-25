from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response, HTTPException

from config import COOKIES_KEY_NAME
from src.models.session import UserSession
from src.repositories.session import SessionRepository
from schemas.user import Session


class SessionService:

    @staticmethod
    async def create(session:AsyncSession, user_session:UserSession):
        add_session_data = user_session.model_dump(exclude_unset=True)
        return await SessionRepository.create(session,add_session_data)

    @staticmethod
    async def get_session_by_cookies(session: AsyncSession, response:Response, cookies: str):
        user_session = await SessionRepository.get_session_by_id(session, cookies)
        if user_session is None:
            response.delete_cookie(COOKIES_KEY_NAME)
            raise HTTPException(status_code=404, detail="Сессия не найдена", headers=response.headers)
        return user_session

    @staticmethod
    async def delete(session: AsyncSession, user_session: Session):
        await SessionRepository.delete(session, user_session)
        return {"detail":"Сессия удалена", "data":None}