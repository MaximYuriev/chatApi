from typing import Sequence

from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import Chat


class ChatRepository:

    @staticmethod
    async def create(session: AsyncSession, add_chat_data: dict) -> None:
        chat = Chat(**add_chat_data)
        session.add(chat)
        await session.commit()

    @staticmethod
    async def get_chat(session: AsyncSession, chat_id: int) -> Chat|None:
        return await session.get(Chat, chat_id)

    @staticmethod
    async def get_chat_between_users(session:AsyncSession, user_1_id: int, user_2_id: int) -> Chat|None:
        query = (
            select(Chat)
            .where(or_(
                and_(Chat.user_1_id == user_1_id, Chat.user_2_id == user_2_id),
                and_(Chat.user_1_id == user_2_id, Chat.user_2_id == user_1_id)
            ))
        )
        return await session.scalar(query)


    @staticmethod
    async def get_all_users_chat(session: AsyncSession, user_id: int) -> Sequence:
        query = (
            select(Chat)
            .where(or_(Chat.user_1_id == user_id, Chat.user_2_id == user_id))
        )
        chats = await session.execute(query)
        return chats.scalars().all()