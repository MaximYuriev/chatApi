from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    content: str = Field(description="Текст сообщения")


class MessageSchema(MessageCreate):
    message_id: int | None = Field(description="id сообщения", serialization_alias="messageId", default=None)
    sender_id: int = Field(description="id отправителя", serialization_alias="senderId")
