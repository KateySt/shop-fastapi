from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exception import NotFoundError, ValidationError
from app.exception.custom_error import AlreadyExistsError


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.detail},
        )

    @app.exception_handler(NotFoundError)
    async def not_found_error_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": exc.detail}
        )

    @app.exception_handler(AlreadyExistsError)
    async def already_exists_error_handler(request: Request, exc: AlreadyExistsError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content={"detail": exc.detail}
        )
