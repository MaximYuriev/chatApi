from fastapi import APIRouter
from fastapi.params import Depends

from dependencies.auth import current_user
from dependencies.user import create_message_data, validate_verify_code
from bgtask.task import send_email_message
from models.user import User
from schemas.user import UserUpdate
from services.user import UserService

user_router = APIRouter(prefix='/user', tags=['User'], dependencies=[Depends(current_user)])


@user_router.get("/verify")
def get_verify_code(message_data: dict = Depends(create_message_data)):
    send_email_message.delay(message_data)
    return {"detail": f"Письмо отправлено на почту!", "data": None}

@user_router.post("/verify", dependencies=[Depends(validate_verify_code)])
async def verify_account(
        user: User = Depends(current_user),
        user_service: UserService = Depends()
):
    await user_service.update(user, UserUpdate(is_verify=True))
    return {"detail": "Аккаунт верифицирован!", "data": None}


@user_router.get("/id")
def get_user_id(user: User = Depends(current_user)):
    return {"detail": "Id текущего пользователя", "data": user.user_id}
