from typing import List
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.functions import ST_Transform, ST_SetSRID, ST_DWithin

from app.models.models import Organization, Activity, Building, organization_activity


async def get_organizations_in_radius_from_db(
        db: AsyncSession, lat: float, lon: float, radius: float) -> List[Organization]:
    """Запрос объектов организаций по коду вида деятельности"""
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


async def get_organizations_by_activity_path_from_db(db: AsyncSession, path: str) -> List[Organization]:
    """Запрос объектов организаций по пути вида деятельности.
    Возвращает все организации с видом деятельности,
    путь которого, начинается с переданного значения пути.
    Таким образом находятся подкатегории видов деятельности.
    """
    async with (db.begin()):
        stmt = (
            select(Organization)
            .join(organization_activity)
            .join(Activity, organization_activity.c.activity_id == Activity.id)
            .filter(Activity.path.startswith(path))
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phone_numbers),
            )
        )

        result = await db.execute(stmt)
    return list(result.scalars().all())
