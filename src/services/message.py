from sqlalchemy.ext.asyncio import AsyncSession

from schemas.chat import ChatOuterRead, ChatInnerRead
from services.chat import ChatServices
from services.ws import WebSocketServices
from src.schemas.message import MessageCreate
from repositories.message import MessageRepository


class MessageService:

    @staticmethod
    async def send_message(session:AsyncSession, message:MessageCreate, sender_id: int, chat:ChatInnerRead):
        message = message.model_dump()
        message.update(sender_id=sender_id)

        if (chat.user_1_id in WebSocketServices.active_connections and
                ChatServices.chat_connections[chat.user_1_id] == chat.chat_id):
            await WebSocketServices.send_message(chat.user_1_id, message)

        if (chat.user_2_id in WebSocketServices.active_connections and
                ChatServices.chat_connections[chat.user_2_id] == chat.chat_id):
            await WebSocketServices.send_message(chat.user_2_id, message)

        message.update(chat_id=chat.chat_id)
        await MessageRepository.create(session, message)

        return {"detail": "Сообщение успешно отправлено", "data":None}

    @staticmethod
    async def get_message_by_chat_id(session:AsyncSession, chat_id: int):
        message_list = await MessageRepository.get_message_between_users(session, chat_id)
        return {"detail":"Диалог между пользователями", "data":message_list}
