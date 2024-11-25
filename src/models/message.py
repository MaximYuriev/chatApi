import datetime

from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from models.user import User, Chat


class Message(Base):
    __tablename__ = 'message'
    message_id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey(Chat.chat_id))
    sender_id: Mapped[int] = mapped_column(ForeignKey(User.user_id))
    content: Mapped[str]
    is_read: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=False), default=datetime.datetime.utcnow())
