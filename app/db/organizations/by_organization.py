from typing import List
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Organization


async def get_organization_by_id_from_db(db: AsyncSession, organization_id: int) -> Organization or None:
    """Запрос объекта организации по id"""
    async with (db.begin()):
        stmt = (
            select(Organization)
            .filter(Organization.id == organization_id)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phone_numbers),
            )
        )

        result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def search_organizations_by_name_from_db(db: AsyncSession, organization_name: str) -> List[Organization]:
    """Запрос объектов организаций по названию"""
    async with (db.begin()):
        stmt = (
            select(Organization)
            .filter(Organization.name.ilike(f"%{organization_name}%"))  # Поиск по названию с учетом регистра
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phone_numbers),
            )
        )

        result = await db.execute(stmt)
    return list(result.scalars().all())
