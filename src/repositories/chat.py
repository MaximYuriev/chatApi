from typing import Sequence

from fastapi import Depends
from sqlalchemy import select, or_, and_, case, desc
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_session
from models.message import Message
from models.user import Chat, User


class ChatRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create(self, add_chat_data: dict) -> None:
        chat = Chat(**add_chat_data)
        self.session.add(chat)
        await self.session.commit()

    async def get_chat(self, chat_id: int) -> Chat | None:
        return await self.session.get(Chat, chat_id)

    async def get_chat_between_users(self, user_1_id: int, user_2_id: int) -> Chat | None:
        query = (
            select(Chat)
            .where(or_(
                and_(Chat.user_1_id == user_1_id, Chat.user_2_id == user_2_id),
                and_(Chat.user_1_id == user_2_id, Chat.user_2_id == user_1_id)
            ))
        )
        return await self.session.scalar(query)

    async def get_all_users_chat(self, user_id: int) -> Sequence:
        cte = (
            select(Chat.chat_id, case(
                (Chat.user_1_id != user_id, Chat.user_1_id),
                (Chat.user_2_id != user_id, Chat.user_2_id),
                else_=user_id
            ).label("user_id"))
            .where(or_(Chat.user_1_id == user_id, Chat.user_2_id == user_id))
            .cte("user_chats")
        )
        subquery = (
            select(Message.chat_id, Message.message_id, Message.content)
            .distinct(Message.chat_id)
            .order_by(Message.chat_id, desc(Message.message_id))
            .cte("last_messages")
        )
        query = (
            select(cte.c.chat_id, case(
                (and_(User.firstname != None, User.lastname != None), User.firstname + " " + User.lastname),
                (and_(User.firstname != None, User.lastname == None), User.firstname),
                (and_(User.firstname == None, User.lastname != None), User.lastname),
                else_=User.username
            ).label("fullname"), subquery.c.content)
            .join(User, User.user_id == cte.c.user_id)
            .join(subquery, cte.c.chat_id == subquery.c.chat_id, isouter=True)
            .order_by(desc(subquery.c.message_id))
        )
        chats = await self.session.execute(query)
        return chats.all()
