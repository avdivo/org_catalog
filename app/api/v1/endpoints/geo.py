from typing import List
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from .docs import Docs
from app.core.database import get_db
from app.schemas.schemas import OrganizationBase
from app.services.organization import get_organizations_in_radius, get_organizations_in_rectangle

router = APIRouter(prefix="/geo", tags=["Geolocation"])


@router.get("/radius", **Docs.RADIUS, response_model=List[OrganizationBase])
async def organizations_in_radius(
        lat: float = Path(..., description="Широта"),
        lon: float = Path(..., description="Долгота"),
        radius: float = Path(..., description="Радиус (метры)"),
        db: AsyncSession = Depends(get_db)):
    """Список организаций в заданном радиусе от точки"""
    return await get_organizations_in_radius(db, lat, lon, radius)


@router.get("/rectangle", **Docs.RECTANGLE, response_model=List[OrganizationBase])
async def organizations_in_rectangle(
        top_left_lat: float = Path(..., description="Широта левой верхней точки"),
        top_left_lon: float = Path(..., description="Долгота левой верхней точки"),
        bottom_right_lat: float = Path(..., description="Широта правой нижней точки"),
        bottom_right_lon: float = Path(..., description="Долгота правой нижней точки"),
        db: AsyncSession = Depends(get_db)
):
    """Список организаций в заданной прямоугольной области"""
    return await get_organizations_in_rectangle(db, top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon)
