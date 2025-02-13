from fastapi import FastAPI

from app.core.config import Config
from app.api.v1.endpoints import organizations, activity, geo, buildings

app = FastAPI(title="Каталог организаций")

app.include_router(organizations.router, prefix="/api/v1")
app.include_router(activity.router, prefix="/api/v1")
app.include_router(geo.router, prefix="/api/v1")
app.include_router(buildings.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",  # Путь к приложению
        host="0.0.0.0",  # Хост
        port=int(Config.APP_PORTS),  # Порт
        reload=True  # Для автоперезагрузки при изменениях в коде
    )
