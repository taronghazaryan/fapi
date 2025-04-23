import json

from fastapi import APIRouter

from starlette.responses import JSONResponse
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from app.repository.async_unit_to_work import AsyncUnitOfWork
from app.repository.message_repository import MessageRepository
from app.services.message_service import MessageService

from app.repository.models import MessageModel, DialogModel

from app.schemas.message import DialogSchema, MessageSchema

from app.managers.redis_manager import RedisCache

dialog_cache = RedisCache()



router = APIRouter(
    prefix='/chat',
    tags=['chat']
)

connections: dict[str, WebSocket] = {}

@router.post('/')
async def start(dialog: DialogSchema):
    async with AsyncUnitOfWork() as uow:
        repo = MessageRepository(uow.session)
        service = MessageService(repo)

        dialog_obj = await service.get_dialog(dialog)

        if dialog_obj:
            return JSONResponse({"message": f"Dialog //{dialog_obj}// already exists"}, status_code=400)

        new_dialog = await service.create_dialog(dialog)
        await uow.commit()

        return JSONResponse({"dialog_id": new_dialog}, status_code=201)



@router.websocket('/ws/{dialog_id}/{user_id}')
async def websocket_endpoint(websocket: WebSocket, dialog_id: str, user_id: str):
    from_user_id = user_id

    allowed = await dialog_cache.is_user_allowed(dialog_id, from_user_id)

    if not allowed:
        async with AsyncUnitOfWork() as uow:
            repo = MessageRepository(uow.session)
            message_service = MessageService(repo)
            dialog = await message_service.get_dialog_from_id(dialog_id)

            if not dialog:
                await websocket.close(code=403)
                return

            await dialog_cache.cache_users(
                dialog_id,
                str(dialog.from_user),
                str(dialog.to_user)
            )

            allowed = from_user_id in [str(dialog.from_user), str(dialog.to_user)]
            if not allowed:
                await websocket.close(code=403)
                return

    await websocket.accept()
    connections[from_user_id] = websocket

    try:
        async with AsyncUnitOfWork() as uow:
            repo = MessageRepository(uow.session)
            message_service = MessageService(repo)
            dialog = await message_service.get_dialog_from_id(dialog_id)


            while True:
                data = await websocket.receive_text()
                message = str(data)

                message_obj = await message_service.create_message(
                    MessageSchema(
                        dialog_id=dialog_id,
                        from_user=from_user_id,
                        message=message
                    )
                )

                await websocket.send_text(json.dumps({
                    "message": message_obj.message,
                    "from_user": from_user_id,
                    "dialog_id": dialog_id,
                }))


                cached_users = await dialog_cache.get_users(dialog_id)
                to_user = cached_users[0] if cached_users[0] != from_user_id else cached_users[1]
                to_ws = connections.get(to_user)
                if to_ws:
                    await to_ws.send_text(json.dumps({
                        "message": message_obj.message,
                        "user_id": from_user_id,
                        "dialog_id": dialog_id,
                    }))

                await uow.commit()

    except WebSocketDisconnect:
        connections.pop(from_user_id, None)

