import asyncio
from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self._user_connections: dict[str, set[WebSocket]] = defaultdict(set)
        self._rooms: dict[str, set[str]] = defaultdict(set)
        self._channels: dict[str, set[str]] = defaultdict(set)

    async def connect(self, websocket: WebSocket, user_id: str) -> None:
        await websocket.accept()
        self._user_connections[user_id].add(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str) -> None:
        self._user_connections[user_id].discard(websocket)
        if not self._user_connections[user_id]:
            del self._user_connections[user_id]
            for members in self._rooms.values():
                members.discard(user_id)
            for subscribers in self._channels.values():
                subscribers.discard(user_id)

    def join_room(self, user_id: str, room_id: str) -> None:
        self._rooms[room_id].add(user_id)

    def leave_room(self, user_id: str, room_id: str) -> None:
        self._rooms[room_id].discard(user_id)
        if not self._rooms[room_id]:
            del self._rooms[room_id]

    def subscribe(self, user_id: str, channel: str) -> None:
        self._channels[channel].add(user_id)

    def unsubscribe(self, user_id: str, channel: str) -> None:
        self._channels[channel].discard(user_id)

    async def send_to_user(self, user_id: str, message: dict) -> None:
        dead: set[WebSocket] = set()
        for ws in self._user_connections.get(user_id, set()):
            try:
                await ws.send_json(message)
            except Exception:
                dead.add(ws)
        for ws in dead:
            self._user_connections[user_id].discard(ws)

    async def broadcast_to_room(
        self, room_id: str, message: dict, exclude_user: str | None = None
    ) -> None:
        tasks = [
            self.send_to_user(uid, message)
            for uid in self._rooms.get(room_id, set())
            if uid != exclude_user
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def broadcast_to_channel(
        self, channel: str, message: dict, exclude_user: str | None = None
    ) -> None:
        tasks = [
            self.send_to_user(uid, message)
            for uid in self._channels.get(channel, set())
            if uid != exclude_user
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def broadcast_all(self, message: dict) -> None:
        tasks = [self.send_to_user(uid, message) for uid in self._user_connections]
        await asyncio.gather(*tasks, return_exceptions=True)

    @property
    def active_users(self) -> int:
        return len(self._user_connections)

    def room_members(self, room_id: str) -> list[str]:
        return list(self._rooms.get(room_id, set()))


manager = ConnectionManager()
