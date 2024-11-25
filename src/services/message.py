from fastapi import Depends

from schemas.chat import ChatSchema
from services.chat import ChatService
from services.ws import WebSocketServices
from src.schemas.message import MessageCreate
from repositories.message import MessageRepository


class MessageService:
    def __init__(self, repository: MessageRepository = Depends()):
        self.repository = repository

    async def send_message(self, message: MessageCreate, sender_id: int, chat: ChatSchema):
        message = message.model_dump()
        message.update(sender_id=sender_id)

        if (chat.user_1_id in WebSocketServices.active_connections and
                ChatService.chat_connections[chat.user_1_id] == chat.chat_id):
            is_connect = await WebSocketServices.send_message(chat.user_1_id, message)
            if sender_id != chat.user_1_id and is_connect:
                message.update(is_read=True)

        if (chat.user_2_id in WebSocketServices.active_connections and
                ChatService.chat_connections[chat.user_2_id] == chat.chat_id):
            is_connect = await WebSocketServices.send_message(chat.user_2_id, message)
            if sender_id != chat.user_2_id and is_connect:
                message.update(is_read=True)

        message.update(chat_id=chat.chat_id)
        await self.repository.create(message)
        return {"detail": "Сообщение успешно отправлено", "data": None}

    async def get_messages_from_chat(self, chat_id: int):
        message_list = await self.repository.get_message_between_users(chat_id)
        return {"detail": "Диалог между пользователями", "data": message_list}

    async def get_all_unread_messages(self, chat_id: int, user_id: int) -> list:
        message_list = await self.repository.get_all_unread_messages(chat_id, user_id)
        return message_list

    async def read_messages(self, messages: list):
        await self.repository.read_all_message(messages)