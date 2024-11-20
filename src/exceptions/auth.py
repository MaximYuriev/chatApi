from fastapi import HTTPException, status


class EmailAlreadyExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Данная почта зарегистрирована в системе!")


class UsernameAlreadyExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Имя пользователя занято!")


class EmailNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь с данной почтой не найден!")


class InvalidPassword(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Неверный пароль!")


class NotAuthorized(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не авторизован!")


class SessionNotFound(HTTPException):
    def __init__(self, headers: dict[str, str] | None = None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Сессия не найдена!", headers=headers)
