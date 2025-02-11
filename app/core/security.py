import os
from fastapi import HTTPException, Request

from .config import Config


def verify_api_key(request: Request):
    """Проверка API ключа"""
    # Получаем ключ из заголовка запроса
    api_key = request.headers.get("X-API-KEY")

    # Проверяем, что ключ существует и он правильный
    if api_key != Config.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return True
