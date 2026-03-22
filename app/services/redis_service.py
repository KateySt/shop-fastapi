import datetime as dt

import redis.asyncio as redis  # type: ignore[import-untyped]
from redis.asyncio import ConnectionPool  # type: ignore[import-untyped]

from app.config import redis_config


class RedisService:
    def __init__(self):
        self._pool = ConnectionPool(
            host=redis_config.REDIS_HOST,
            port=redis_config.REDIS_PORT,
            username=redis_config.REDIS_USER,
            password=redis_config.REDIS_PASSWORD,
            db=redis_config.REDIS_DATABASE,
            decode_responses=True,
            max_connections=10,
        )
        self.redis = redis.Redis(connection_pool=self._pool)

    async def close(self):
        await self._pool.disconnect()

    async def set_cache(self, key: str, value: str | int, ttl: int = 60) -> None:
        await self.redis.setex(key, dt.timedelta(seconds=ttl), value)

    async def get_cache(self, key: str) -> str | None:
        return await self.redis.get(key)

    async def delete_cache(self, key: str) -> None:
        await self.redis.delete(key)
