from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.models.models import Organization

async def get_organization_by_id(db: AsyncSession, organization_id: int) -> Organization or None:
    """Получение объекта организации по id"""
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
        organization = result.scalar_one_or_none()

        if organization is None:
            raise HTTPException(status_code=404, detail="Организация не найдена")

        return organization

