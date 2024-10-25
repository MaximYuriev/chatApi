from httpx import AsyncClient


async def test_create_new_chat(client: AsyncClient, current_test_user):
    chat_create = {"user2Id": 2}
    response = await client.post("/chat", json=chat_create)
    assert response.status_code == 200

    response = await client.post("/chat", json=chat_create)
    assert response.status_code == 400

    response = await client.get("/chat")
    assert response.status_code == 200

    response = await client.get("/chat/1")
    assert response.status_code == 200

async def test_send_message(client: AsyncClient, current_test_user):
    message = {"content": "string"}
    response = await client.post("/chat/message/1", json=message)
    assert response.status_code == 200

    response = await client.get("/chat/message/1")
    assert response.status_code == 200

    response = await client.post("/chat/message/221", json=message)
    assert response.status_code == 404