from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    email: EmailStr = Field(description="Электронная почта пользователя")
    password: str = Field(description="Пароль пользователя")

class User(UserLogin):
    username: str = Field(min_length=1, max_length=15)
    firstname: str|None = Field(min_length=1, max_length=15, default=None)
    lastname: str|None = Field(min_length=1, max_length=15, default=None)

class UserUpdate(User):
    username: str|None = Field(min_length=1, max_length=15, default=None)
    email: EmailStr|None = None
    password: str|None = None
    is_verify: bool|None = None

class UserRead(BaseModel):
    user_id: int = Field(description="Id пользователя")
    username: str
    firstname: str|None = Field(default=None)
    lastname: str|None = Field(default=None)