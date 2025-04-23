import asyncio
import json

from fastapi import WebSocket

from app.repository.message_repository import MessageRepository
from app.repository.async_unit_to_work import AsyncUnitOfWork
from app.services.message_service import MessageService


class WebSocketManager:
    def __init__(self, dialog_id: str):
        self.connections: dict = {}  # stores user_guid: {ws1, ws2} combinations
        self.dialog_id = dialog_id

    async def get_users(self, websocket: WebSocket):
        async with AsyncUnitOfWork() as uow:
            repo = MessageRepository(uow.session)
            service = MessageService(repo)

            dialog = await service.get_dialog_from_id(self.dialog_id)
            if dialog:
                self.connections[dialog.from_user] = websocket
                self.connections[dialog.to_user] = websocket


    async def connect_socket(self, websocket: WebSocket):
        await websocket.accept()


    async def send_error(self, message: str, websocket: WebSocket):
        await websocket.send_json({"status": "error", "message": message})