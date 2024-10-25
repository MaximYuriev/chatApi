from fastapi import Request, Depends, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config import COOKIES_KEY_NAME
from db.database import get_session
from schemas.user import Session
from services.session import SessionService
from src.services.user import UserService

def find_cookies(request: Request):
    cookie_session_id = request.cookies.get(COOKIES_KEY_NAME)
    return cookie_session_id

async def current_session(response:Response, session: AsyncSession = Depends(get_session),
                          cookies: str|None = Depends(find_cookies)):
    if cookies is None:
        raise HTTPException(status_code=403, detail="Необходимо выполнить вход")
    return await SessionService.get_session_by_cookies(session, response, cookies)

async def current_user(user_session: Session = Depends(current_session),session: AsyncSession = Depends(get_session)):
    return await UserService.get_user_by_session(session, user_session)