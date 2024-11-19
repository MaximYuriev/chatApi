import uuid
from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base


class User(Base):
    __tablename__ = 'user'
    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]
    firstname: Mapped[str] = mapped_column(nullable=True)
    lastname: Mapped[str] = mapped_column(nullable=True)
    is_verify: Mapped[bool] = mapped_column(default=False)


class Chat(Base):
    __tablename__ = 'chat'
    chat_id: Mapped[int] = mapped_column(primary_key=True)
    user_1_id: Mapped[int] = mapped_column(ForeignKey(User.user_id))
    user_2_id: Mapped[int] = mapped_column(ForeignKey(User.user_id))


class Session(Base):
    __tablename__ = "session"
    session_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.user_id, ondelete="CASCADE"))
    user_agent: Mapped[str] = mapped_column(nullable=True)
