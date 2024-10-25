from httpx import AsyncClient


async def test_registration(client: AsyncClient):
    user = {
        "email": "user@example.com",
        "password": "string",
        "username": "string"
    }
    response = await client.post("/auth/registration", json=user)
    assert response.status_code == 200

    user.update(firstname="firstname", lastname="lastname")
    response = await client.post("/auth/registration", json=user)
    assert response.status_code == 400

    user['email'] = "user@example2.com"
    response = await client.post("/auth/registration", json=user)
    assert response.status_code == 400

    user['username'] = "new_username"
    response = await client.post("/auth/registration", json=user)
    assert response.status_code == 200


async def test_login(client: AsyncClient):
    user = {
        "email": "user@example.com",
        "password": "string"
    }
    response = await client.post("/auth/login", json=user)
    assert response.status_code == 200


async def test_logout(client: AsyncClient):
    response = await client.get("/auth/logout")
    assert response.status_code == 200
