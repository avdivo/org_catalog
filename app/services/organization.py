from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Organization
from app.db.by_organization import get_organization_by_id_from_db, search_organizations_by_name_from_db
from app.db.by_activity import get_organizations_by_activity_id_from_db, get_organizations_by_activity_id_deep_from_db


async def get_organization_by_id(db: AsyncSession, organization_id: int) -> Organization or None:
    """Получение объекта организации по id"""
    organization = await get_organization_by_id_from_db(db, organization_id)
    if organization is None:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return organization


async def search_organization_by_name(db: AsyncSession, organization_name: str) -> List[Organization]:
    """Поиск организации по имени"""
    return await search_organizations_by_name_from_db(db, organization_name)


async def get_organizations_by_activity_id(db: AsyncSession, activity_id: int) -> List[Organization]:
    """Поиск организаций по коду вида деятельности"""
    return await get_organizations_by_activity_id_from_db(db, activity_id)


async def get_organizations_by_activity_id_deep(db: AsyncSession, activity_id: int) -> List[Organization]:
    """Поиск организаций по коду вида деятельности включая подкатегории"""
    return await get_organizations_by_activity_id_deep_from_db(db, activity_id)
