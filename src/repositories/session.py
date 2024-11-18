import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response, Request, Depends

from config import COOKIES_KEY_NAME
from db.database import get_session
from models.user import Session


class SessionRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create(self, add_session_data:dict) -> uuid.UUID:
        user_session = Session(**add_session_data)
        self.session.add(user_session)
        await self.session.commit()
        return user_session.session_id

    async def get_session_by_id(self, session_id: uuid.UUID | str) -> Session | None:
        return await self.session.get(Session, session_id)

    async def delete(self, user_session:Session) -> None:
        await self.session.delete(user_session)
        await self.session.commit()

class SessionCookieRepository:
    def __init__(self, response: Response, request: Request):
        self.response = response
        self.request = request

    def create(self, session_id: uuid.UUID | str):
        self.response.set_cookie(COOKIES_KEY_NAME, value=session_id, httponly=True)

    def get(self):
        return self.request.cookies.get(COOKIES_KEY_NAME)

    def delete(self):
        self.response.delete_cookie(COOKIES_KEY_NAME)
        return self.response.headers