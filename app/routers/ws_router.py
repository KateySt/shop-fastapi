import asyncio
import json

from fastapi import APIRouter, Depends, WebSocket

from app.db.models import User
from app.dependencies import Pagination
from app.dependencies.auth import get_current_user, get_ws_user
from app.schemas import WSIncomingMessage
from app.services import WSServiceDep
from app.websockets.connection_manager import manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    service: WSServiceDep,
    user: User = Depends(get_ws_user),
):
    user_id = str(user.id)
    await manager.connect(websocket, user_id)
    ping_task = asyncio.create_task(_ping_loop(websocket))

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                msg = WSIncomingMessage(**json.loads(raw))
            except Exception:
                await websocket.send_json(
                    {
                        "type": "error",
                        "payload": "Invalid message format",
                    }
                )
                continue

            await service.handle_message(msg, user)
    finally:
        ping_task.cancel()
        manager.disconnect(websocket, user_id)


@router.get("/ws/history/room/{room}")
async def room_history(
    room: str,
    service: WSServiceDep,
    pagination: Pagination,
    user: User = Depends(get_current_user),
):
    return await service.get_room_history(room, pagination)


@router.get("/ws/history/channel/{channel}")
async def channel_history(
    channel: str,
    service: WSServiceDep,
    pagination: Pagination,
    user: User = Depends(get_current_user),
):
    return await service.get_channel_history(channel, pagination)


async def _ping_loop(websocket: WebSocket, interval: int = 30) -> None:
    while True:
        await asyncio.sleep(interval)
        await websocket.send_json({"type": "ping"})
