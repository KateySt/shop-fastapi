from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import app_config
from app.exception import register_exception_handlers
from app.routers import auth_router, company_router, item_router, user_router
from app.services import init_sentry

init_sentry()


def get_application() -> FastAPI:
    app = FastAPI(
        title=app_config.APP_NAME,
        debug=app_config.DEBUG,
        root_path="/api",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    app.include_router(company_router, prefix="/companies", tags=["companies"])
    app.include_router(item_router, prefix="/items", tags=["items"])
    app.include_router(auth_router, prefix="/auth", tags=["Auth"])
    app.include_router(user_router, prefix="/users", tags=["User"])

    return app
