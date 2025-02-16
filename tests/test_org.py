import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.core.config import Config


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/api/v1/organizations/1")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.asyncio
@pytest.mark.parametrize("org_id, expected_name", [(1, "Мясной Двор")])
async def test_get_organization(org_id, expected_name):
    """Тестирование получения организаций по ID"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get(f"/api/v1/organizations/{org_id}", headers={"X-API-KEY": Config.API_KEY})
    assert response.status_code == 200
    assert response.json()["name"] == expected_name


