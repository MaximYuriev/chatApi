from pydantic import BaseModel, Field


class ChatCreate(BaseModel):
    user_2_id: int = Field(description="id друга", validation_alias="user2Id")

class ChatRead(BaseModel):
    chat_id: int = Field(description="id чата", serialization_alias="chatId")
    user_1_id: int = Field(description="id создателя чата", serialization_alias="user1Id")
    user_2_id: int = Field(description="id друга", serialization_alias="user2Id")