from pydantic import BaseModel, Field


class UserSession(BaseModel):
    user_id: int = Field(description="id пользователя")
    user_agent: str|None = Field(default=None, description="User-Agent из заголовков браузера")