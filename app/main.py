import logging
from fastapi import FastAPI

from app.core.config import Config
from app.api.v1.endpoints import organizations, activity, geo, buildings

logging.basicConfig(level=logging.INFO)  # Лог файл не создается, логи выводятся в консоль
# Добавляем FileHandler для записи логов в файл
file_handler = logging.FileHandler("app.log", encoding="utf-8")
logging.getLogger().addHandler(file_handler)

app = FastAPI(title="Каталог организаций")

app.include_router(organizations.router, prefix="/api/v1")
app.include_router(activity.router, prefix="/api/v1")
app.include_router(geo.router, prefix="/api/v1")
app.include_router(buildings.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=int(Config.APP_PORTS), reload=True)
