from openai import OpenAI

from config import OPEN_AI_KEY


class BotService:
    client = OpenAI(
        api_key=OPEN_AI_KEY,
        base_url="https://api.vsegpt.ru/v1",
    )

    @classmethod
    def generate_response(cls, message: str):
        messages = [{"role": "user", "content": message}]
        response_big = cls.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        response = response_big.choices[0].message.content
        return response
