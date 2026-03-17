from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exception.custom_error import CustomError


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(CustomError)
    async def app_error_handler(request: Request, exc: CustomError):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
