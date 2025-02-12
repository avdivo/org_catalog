from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.main import app


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"Ошибка: {exc.detail}"},
    )


@app.exception_handler(Exception)
async def universal_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Произошла внутренняя ошибка сервера"},
    )
