from fastapi import APIRouter, Request, Depends
from starlette.templating import Jinja2Templates

from dependencies.auth import current_user
from routers.chat import get_all_users_chats, get_chat_by_chat_id
from models.user import User, Chat

page_router = APIRouter(prefix="/page", tags=['Pages'])

templates = Jinja2Templates(directory='templates')

@page_router.get("")
def get_main_page(request: Request, user:User = Depends(current_user), chats:list = Depends(get_all_users_chats)):
    return templates.TemplateResponse("main_page.html", {"request": request, "current_user":user, "chats":chats})

@page_router.get("/chat/{chat_id}")
def get_chat_page(request: Request, user:User = Depends(current_user),
                  chats:list = Depends(get_all_users_chats), chat:Chat = Depends(get_chat_by_chat_id)):
    return templates.TemplateResponse("chat.html", {"request": request, "current_user": user,
                                                    "chats": chats, "current_chat": chat})