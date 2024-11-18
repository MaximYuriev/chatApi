from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    content: str = Field(description="Текст сообщения")

class MessageRead(MessageCreate):
    message_id: int = Field(description="id сообщения", serialization_alias="messageId")
    sender_id: int = Field(description="id отправителя", serialization_alias="senderId")