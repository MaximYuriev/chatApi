from fastapi import Depends
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_session
from src.schemas.message import MessageSchema
from models.message import Message


class MessageRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create(self, add_data_message: dict) -> None:
        message = Message(**add_data_message)
        self.session.add(message)
        await self.session.commit()

    async def get_message_between_users(self, chat_id: int) -> list:
        query = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.message_id)
        )
        res = await self.session.execute(query)
        result_orm = res.scalars().all()
        result_dto = [MessageSchema.model_validate(row, from_attributes=True) for row in result_orm]
        return result_dto

    async def get_all_unread_messages(self, chat_id: int, user_id: int):
        query = (
            select(Message)
                 .where(and_(Message.chat_id == chat_id, Message.is_read == False, Message.sender_id != user_id))
        )
        return await self.session.scalars(query)

    async def read_all_message(self, messages: list):
        for message in messages:
            message.is_read = True
        await self.session.commit()