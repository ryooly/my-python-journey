from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions.base import AppException


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.message,
        },
    )
