import random

from fastapi import HTTPException

from repositories.user import UserRedisRepository


class UserRedisService:
    @staticmethod
    def generation_verify_code(user_id: int):
        code_value = random.randint(1000, 9999)
        UserRedisRepository.set(key=str(user_id), value=code_value, expire=300)
        return code_value

    @staticmethod
    def get(user_id: int) -> int | None:
        return UserRedisRepository.get(str(user_id))

        if true_code != user_code:
            raise HTTPException(status_code=400, detail="Введен неверный код!")
