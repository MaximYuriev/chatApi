from fastapi import HTTPException, Depends

from exceptions.auth import SessionNotFound
from repositories.session import SessionRepository, SessionCookieRepository
from src.schemas.session import UserSession
from models.user import Session


class SessionService:
    def __init__(self, db_repository: SessionRepository = Depends(), cookie_repository: SessionCookieRepository = Depends()):
        self.repository = db_repository
        self.cookie_storage = cookie_repository

    async def create(self, user_session:UserSession):
        add_session_data = user_session.model_dump(exclude_unset=True)
        session_id = await self.repository.create(add_session_data)
        self.cookie_storage.create(session_id)

    def get_cookie(self):
        return self.cookie_storage.get()

    async def get_session(self, cookies: str):
        user_session = await self.repository.get_session_by_id(cookies)
        if user_session is None:
            headers = self.cookie_storage.delete()
            raise SessionNotFound(headers=headers)
        return user_session

    async def delete(self, user_session: Session):
        await self.repository.delete(user_session)

    async def delete_with_cookie(self, user_session: Session):
        await self.delete(user_session)
        self.cookie_storage.delete()