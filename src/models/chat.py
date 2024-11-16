from pydantic import BaseModel, Field


class ChatCreate(BaseModel):
    username: str = Field(description="Имя пользователя")

class ChatOuterRead(BaseModel):
    chat_id: int = Field(description="id чата", serialization_alias="chatId")
    fullname: str = Field(description="Полное имя пользователя")
    last_message: str | None = Field(description="Последнее сообщение",
                                     serialization_alias="lastMessage",
                                     validation_alias="content")

class ChatInnerRead(BaseModel):
    chat_id: int
    user_1_id: int
    user_2_id: int