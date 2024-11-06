from pydantic import BaseModel, Field


class ChatCreate(BaseModel):
    username: str = Field(description="Имя пользователя")

class ChatOuterRead(BaseModel):
    chat_id: int = Field(description="id чата", serialization_alias="chatId")
    fullname: str = Field(description="Полное имя пользователя")

class ChatInnerRead(BaseModel):
    chat_id: int
    user_1_id: int
    user_2_id: int