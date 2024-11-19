from fastapi import HTTPException, status


class ChatAlreadyExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Чат уже существует!")


class ChatNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Чат не найден!")


class ChatAccessDenied(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="У вас нет доступа к этому чату!")
