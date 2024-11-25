import asyncio

from fastapi import WebSocket, WebSocketDisconnect

from services.chat import ChatService


class WebSocketServices:
    active_connections: dict[int, WebSocket] = {}

    @classmethod
    async def ws_connection(cls, websocket: WebSocket, user_id: int, chat_id: int):
        await websocket.accept()
        WebSocketServices.add_on_connection_list(websocket, user_id)
        ChatService.add_on_connection_list(user_id, chat_id)
        try:
            while True:
                await asyncio.sleep(1)
        except WebSocketDisconnect:
            WebSocketServices.ws_disconnect(user_id)

    @classmethod
    async def send_message(cls, user_id: int, message: dict):
        websocket = cls.active_connections[user_id]
        try:
            await websocket.send_json(message)
            return True
        except WebSocketDisconnect:
            WebSocketServices.ws_disconnect(user_id)
            return False

    @classmethod
    def ws_disconnect(cls, user_id: int):
        WebSocketServices.remove_on_connection_list(user_id)
        ChatService.remove_on_connection_list(user_id)

    @classmethod
    def add_on_connection_list(cls, websocket: WebSocket, user_id: int):
        cls.active_connections[user_id] = websocket

    @classmethod
    def remove_on_connection_list(cls, user_id: int):
        cls.active_connections.pop(user_id, None)
