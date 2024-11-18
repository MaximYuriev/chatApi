from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from models.user import User, Chat


class Message(Base):
    __tablename__ = 'message'
    message_id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey(Chat.chat_id))
    sender_id: Mapped[int] = mapped_column(ForeignKey(User.user_id))
    content: Mapped[str]
