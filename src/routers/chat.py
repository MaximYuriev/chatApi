from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_session
from dependencies.dependecies import current_user
from models.chat import ChatCreate, ChatOuterRead, ChatInnerRead
from models.message import MessageCreate
from schemas.user import User, Chat
from services.chat import ChatServices
from services.message import MessageService
from services.ws import WebSocketServices

chat_router = APIRouter(prefix="/chat", tags=["Chat"])

active_connections: dict[int, WebSocket] = {}
chat_connections: dict[int, int] = {}

@chat_router.websocket("/ws/{chat_id}/{user_id}")
async def websocket_connection(websocket: WebSocket, user_id: int, chat_id: int):
    return await WebSocketServices.ws_connection(websocket, user_id, chat_id)

@chat_router.post("")
async def create_new_chat(chat: ChatCreate, user: User = Depends(current_user),
                          session: AsyncSession = Depends(get_session)):
    return await ChatServices.create_chat(session, chat, user.user_id)

@chat_router.get("")
async def get_all_users_chats(user: User = Depends(current_user), session: AsyncSession = Depends(get_session)):
    return await ChatServices.get_all_user_chat(session, user.user_id)

@chat_router.get("/{chat_id}")
async def get_chat_by_chat_id(chat_id:int, user: User = Depends(current_user),
                              session: AsyncSession = Depends(get_session)):
    return await ChatServices.get_chat(session, chat_id, user.user_id)

@chat_router.get("/message/{chat_id}")
async def get_message(user: User = Depends(current_user), chat: ChatOuterRead = Depends(get_chat_by_chat_id),
                      session: AsyncSession = Depends(get_session)):
    return await MessageService.get_message_by_chat_id(session, chat.chat_id)

@chat_router.post("/message/{chat_id}")
async def send_message(message: MessageCreate, user: User = Depends(current_user),
                       chat: ChatInnerRead = Depends(get_chat_by_chat_id), session: AsyncSession = Depends(get_session)):
    await MessageService.send_message(session, message, user.user_id, chat)

