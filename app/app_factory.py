from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.middleware.cors import CORSMiddleware

from app.config import app_config
from app.exception import register_exception_handlers
from app.routers import auth_router, company_router, item_router, user_router
from app.services import init_sentry, redis_service

init_sentry()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis = redis_service.redis
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    await redis.close()
    await redis.connection_pool.disconnect()


def get_application() -> FastAPI:
    app = FastAPI(
        title=app_config.APP_NAME,
        debug=app_config.DEBUG,
        root_path="/api",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    app.include_router(company_router, prefix="/companies", tags=["Companies"])
    app.include_router(item_router, prefix="/items", tags=["Items"])
    app.include_router(auth_router, prefix="/auth", tags=["Auth"])
    app.include_router(user_router, prefix="/users", tags=["Users"])

    return app
