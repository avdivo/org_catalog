from typing import List
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.functions import ST_Transform, ST_SetSRID, ST_DWithin, ST_Within

from app.models.models import Organization, Activity, Building, organization_activity


async def get_organizations_in_radius_from_db(
        db: AsyncSession, lat: float, lon: float, radius: float) -> List[Organization]:
    """Запрос объектов организаций по точке и радиусу на карте"""
    async with (db.begin()):
        stmt = (
            select(Organization)
            .join(Building)
            .filter(
                ST_DWithin(
                    ST_Transform(Building.location, 3857),  # Переводим координаты здания в метры
                    ST_Transform(ST_SetSRID(func.ST_MakePoint(lon, lat), 4326), 3857),
                    # Переводим заданную точку в метры
                    radius  # Радиус в метрах
                )
            )
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phone_numbers),
            )
        )

        result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_organizations_in_rectangle_from_db(
        db: AsyncSession,
        top_left_lat: float, top_left_lon: float,
        bottom_right_lat: float, bottom_right_lon: float
        ) -> List[Organization]:
    """Запрос объектов организаций по прямоугольнику на карте"""
    async with (db.begin()):
        stmt = (
            select(Organization)
            .join(Building)
            .filter(
                ST_Within(
                    Building.location,  # Координаты здания
                    func.ST_MakeEnvelope(bottom_right_lon, bottom_right_lat, top_left_lon, top_left_lat, 4326)
                    # Прямоугольник
                )
            )
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phone_numbers),
            )
        )

        result = await db.execute(stmt)
    return list(result.scalars().all())
