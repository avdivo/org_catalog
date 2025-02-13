import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from .config import Config

DATABASE_URL = (f"postgresql+asyncpg://{Config.DB_USER}:{Config.DB_PASSWORD}"
                f"@{os.getenv('DB_HOST', 'localhost')}:5432/{Config.DB_NAME}")

engine = create_async_engine(DATABASE_URL, echo=False)  # Логи выключены
async_session = async_sessionmaker(engine, expire_on_commit=False)


# Функция для инициализации базы данны3х (создание таблиц)class Base(AsyncAttrs, DeclarativeBase):
class Base(AsyncAttrs, DeclarativeBase):
    pass


# Получение сессии
async def get_db():
    async with async_session() as session:
        yield session
