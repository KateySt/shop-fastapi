from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import app_config
from app.exception import register_exception_handlers
from app.routers import company_router, item_router

app = FastAPI(title=app_config.APP_NAME, root_path="/api")

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
