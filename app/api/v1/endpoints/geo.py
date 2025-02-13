from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .docs import Docs
from app.core.database import get_db
from app.core.security import verify_api_key
from app.schemas.schemas import OrganizationBase
from app.services.organization import get_organizations_in_radius, get_organizations_in_rectangle

router = APIRouter(prefix="/geo", tags=["Geolocation"])


@router.get("/radius", **Docs.RADIUS, response_model=List[OrganizationBase])
async def organizations_in_radius(
        auth: bool = Depends(verify_api_key),
        lat: float = Query(..., description="Широта"),
        lon: float = Query(..., description="Долгота"),
        radius: float = Query(..., description="Радиус (метры)"),
        db: AsyncSession = Depends(get_db)):
    """Список организаций в заданном радиусе от точки"""
    return await get_organizations_in_radius(db, lat, lon, radius)


@router.get("/rectangle", **Docs.RECTANGLE, response_model=List[OrganizationBase])
async def organizations_in_rectangle(
        auth: bool = Depends(verify_api_key),
        top_left_lat: float = Query(..., description="Широта левой верхней точки"),
        top_left_lon: float = Query(..., description="Долгота левой верхней точки"),
        bottom_right_lat: float = Query(..., description="Широта правой нижней точки"),
        bottom_right_lon: float = Query(..., description="Долгота правой нижней точки"),
        db: AsyncSession = Depends(get_db)
):
    """Список организаций в заданной прямоугольной области"""
    return await get_organizations_in_rectangle(db, top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon)
