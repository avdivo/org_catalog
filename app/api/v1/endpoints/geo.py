from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.schemas import OrganizationBase
from app.core.database import get_db
from app.services.organization import get_organizations_in_radius, get_organizations_in_rectangle

router = APIRouter(prefix="/geo", tags=["Geolocation"])


@router.get("/radius", response_model=List[OrganizationBase])
async def organizations_in_radius(lat: float, lon: float, radius: float, db: AsyncSession = Depends(get_db)):
    """Список организаций в заданном радиусе от точки"""
    return await get_organizations_in_radius(db, lat, lon, radius)


@router.get("/rectangle", response_model=List[OrganizationBase])
async def organizations_in_rectangle(
        top_left_lat: float, top_left_lon: float,
        bottom_right_lat: float, bottom_right_lon: float,
        db: AsyncSession = Depends(get_db)
):
    """Список организаций в заданной прямоугольной области"""
    return await get_organizations_in_rectangle(db, top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon)
