import os
from fastapi.security import APIKeyHeader
from fastapi import HTTPException, Depends, HTTPException

from .config import Config

# Определяем схему безопасности для заголовка X-API-KEY
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=True)


def verify_api_key(api_key: str = Depends(api_key_header)):
    """Проверка API ключа"""
    if api_key != Config.API_KEY:
        raise HTTPException(status_code=401, detail="Не верный ключ авторизации")
    return True
