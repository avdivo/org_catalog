from typing import List
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Organization, Activity, organization_activity


async def get_organizations_by_activity_id_from_db(db: AsyncSession, activity_id: int) -> List[Organization]:
    """Запрос объектов организаций по коду вида деятельности"""
    async with (db.begin()):
        stmt = (
            select(Organization)
            .join(organization_activity)
            .filter(organization_activity.c.activity_id == activity_id)
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
