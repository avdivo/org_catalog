from typing import List
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Organization


async def get_organizations_in_building_from_db(db: AsyncSession, building_id: int) -> List[Organization]:
    """Запрос объектов организаций по id здания в котором они находятся"""
    async with (db.begin()):
        stmt = (
            select(Organization)
            .filter(Organization.building_id == building_id)  # Фильтрация по зданию
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phone_numbers),
            )
        )

        result = await db.execute(stmt)
    return list(result.scalars().all())
