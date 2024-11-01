from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.chat import ChatCreate, ChatRead
from repositories.chat import ChatRepository
from src.services.user import UserRepository


class ChatServices:
    chat_connections: dict[int, int] = {}

    @staticmethod
    async def create_chat(session: AsyncSession, chat:ChatCreate, user_id: int):
        if await UserRepository.get_user_by_id(session, chat.user_2_id) is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден!")
        if await ChatRepository.get_chat_between_users(session, user_id, chat.user_2_id):
            raise HTTPException(status_code=400, detail="Чат между пользователями уже создан!")
        chat = chat.model_dump()
        chat["user_1_id"] = user_id
        await ChatRepository.create(session, chat)
        return {"detail":"Чат был успешно создан","data":None}

    @staticmethod
    async def get_all_user_chat(session: AsyncSession, user_id:int):
        chats = await ChatRepository.get_all_users_chat(session, user_id)
        return {
            "detail":"Все чаты пользователя",
            "data":[ChatRead.model_validate(chat, from_attributes=True) for chat in chats]
        }

    @staticmethod
    async def get_chat(session: AsyncSession, chat_id: int, user_id: int):
        chat = await ChatRepository.get_chat(session, chat_id)
        if chat is None:
            raise HTTPException(status_code=404, detail="Чат не найден")
        if chat.user_1_id != user_id and chat.user_2_id != user_id:
            raise HTTPException(status_code=403, detail="У вас нет доступа к этому чату")
        return ChatRead.model_validate(chat, from_attributes=True)

    @classmethod
    def add_on_connection_list(cls, user_id:int, chat_id:int):
        cls.chat_connections[user_id] = chat_id

    @classmethod
    def remove_on_connection_list(cls, user_id: int):
        cls.chat_connections.pop(user_id, None)