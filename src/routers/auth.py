from typing import Annotated

from fastapi import APIRouter, Depends, Response, Header
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_session
from src.dependencies.dependecies import current_session, find_cookies
from schemas.user import Session as SignInSession
from src.models.user import UserLogin
from src.models.user import User as UserDTO
from src.services.user import UserService

auth_router = APIRouter(prefix='/auth', tags=['Auth'])

@auth_router.post('/registration')
async def user_registration(user:UserDTO, session:AsyncSession = Depends(get_session)):
    return await UserService.create(session, user)

@auth_router.post('/login')
async def user_login(user_auth:UserLogin, response:Response, user_agent: Annotated[str | None, Header()] = None,
                     session:AsyncSession = Depends(get_session), cookies: str|None = Depends(find_cookies)):
    return await UserService.login(session,response,user_auth,user_agent, cookies)


@auth_router.get('/logout')
async def user_logout(response:Response, user_session:SignInSession = Depends(current_session),
                      session: AsyncSession = Depends(get_session)):
    return await UserService.logout(session, response, user_session)

