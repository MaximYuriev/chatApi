from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.message import MessageRead
from schemas.message import Message


class MessageRepository:

    @staticmethod
    async def create(session:AsyncSession, add_data_message:dict) -> None:
        message = Message(**add_data_message)
        session.add(message)
        await session.commit()

    @staticmethod
    async def get_message_between_users(session:AsyncSession, chat_id:int) -> list:
        query = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.message_id)
        )
        res = await session.execute(query)
        result_orm = res.scalars().all()
        result_dto = [MessageRead.model_validate(row, from_attributes=True) for row in result_orm]
        return  result_dto