from typing import Annotated

from fastapi import APIRouter, Body
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_session
from dependencies.auth import current_user

from models.user import User
from services.user import UserService

user_router = APIRouter(prefix='/user', tags=['User'])


@user_router.get("/verify")
def get_verify_code(user: User = Depends(current_user)):
    return UserService.send_verify_code(user)


@user_router.post("/verify")
async def verify_account(verify_code: Annotated[int, Body()], user: User = Depends(current_user),
                         session: AsyncSession = Depends(get_session)):
    return await UserService.verify_account(session, user, verify_code)


@user_router.get("/id")
def get_user_id(user: User = Depends(current_user)):
    return {"detail": "Id текущего пользователя", "data": user.user_id}
