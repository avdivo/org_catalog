from fastapi.testclient import TestClient

from app.main import app  # Импортируйте ваше приложение FastAPI
from app.core.config import Config

# Создаем TestClient
client = TestClient(app)


def test_get_organization():
    response = client.get("/api/v1/organizations/1", headers={"X-API-KEY": Config.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Мясной Двор"
    assert data["building"]["address"] == "ул. Тверская, д. 10, Москва"


