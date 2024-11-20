from fastapi import Depends

from exceptions.chat import ChatNotFound, ChatAccessDenied
from models.user import Chat
from schemas.chat import ChatOuterRead, ChatSchema
from repositories.chat import ChatRepository


class ChatService:
    chat_connections: dict[int, int] = {}

    def __init__(self, repository: ChatRepository = Depends()):
        self.repository = repository

    async def create(self, chat_create: ChatSchema):
        chat_data = chat_create.model_dump(exclude_none=True)
        await self.repository.create(chat_data)
        return {"detail": "Чат был успешно создан", "data": None}

    async def get_chat_between_users(self, user_1_id: int, user_2_id: int) -> Chat | None:
        return await self.repository.get_chat_between_users(user_1_id, user_2_id)

    async def get_all_user_chat(self, user_id: int):
        chats = await self.repository.get_all_users_chat(user_id)
        return {
            "detail": "Все чаты пользователя",
            "data": [ChatOuterRead.model_validate(chat, from_attributes=True) for chat in chats]
        }

    async def get_chat(self, chat_id: int, user_id: int):
        chat = await self.repository.get_chat(chat_id)
        if chat is None:
            raise ChatNotFound
        if chat.user_1_id != user_id and chat.user_2_id != user_id:
            raise ChatAccessDenied
        return ChatSchema.model_validate(chat, from_attributes=True)

    @classmethod
    def add_on_connection_list(cls, user_id: int, chat_id: int):
        cls.chat_connections[user_id] = chat_id

    @classmethod
    def remove_on_connection_list(cls, user_id: int):
        cls.chat_connections.pop(user_id, None)
