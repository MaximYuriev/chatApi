from typing import Annotated

from fastapi import APIRouter, WebSocket, Depends

from dependencies.auth import current_user
from dependencies.chat import validate_chat_create
from schemas.chat import ChatSchema
from schemas.message import MessageCreate
from models.user import User
from services.chat import ChatService
from services.message import MessageService
from services.ws import WebSocketServices

chat_router = APIRouter(prefix="/chat", tags=["Chat"])

active_connections: dict[int, WebSocket] = {}
chat_connections: dict[int, int] = {}


@chat_router.websocket("/ws/{chat_id}/{user_id}")
async def websocket_connection(websocket: WebSocket, user_id: int, chat_id: int):
    await WebSocketServices.ws_connection(websocket, user_id, chat_id)


@chat_router.post("")
async def create_new_chat(
        chat: Annotated[ChatSchema, Depends(validate_chat_create)],
        chat_service: ChatService = Depends()
):
    return await chat_service.create(chat)


@chat_router.get("")
async def get_all_users_chats(
        user: User = Depends(current_user),
        chat_service: ChatService = Depends()
):
    return await chat_service.get_all_user_chat(user.user_id)


@chat_router.get("/{chat_id}")
async def get_chat_by_chat_id(
        chat_id: int,
        user: User = Depends(current_user),
        chat_service: ChatService = Depends()
):
    return await chat_service.get_chat(chat_id, user.user_id)


@chat_router.get("/message/{chat_id}")
async def get_message(
        chat: Annotated[ChatSchema, Depends(get_chat_by_chat_id)],
        message_service: MessageService = Depends()
):
    return await message_service.get_messages_from_chat(chat.chat_id)


@chat_router.post("/message/{chat_id}")
async def send_message(
        message: MessageCreate,
        user: User = Depends(current_user),
        chat: ChatSchema = Depends(get_chat_by_chat_id),
        message_service: MessageService = Depends()
):
    return await message_service.send_message(message, user.user_id, chat)

@chat_router.patch("/message/{chat_id}")
async def read_unread_message(
        user: Annotated[User, Depends(current_user)],
        chat_id: int,
        message_service: MessageService = Depends()
):
    messages = await message_service.get_all_unread_messages(chat_id, user.user_id)
    if messages:
        await message_service.read_messages(messages)