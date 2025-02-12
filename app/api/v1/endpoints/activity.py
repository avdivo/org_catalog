from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.database import get_db
from app.schemas.schemas import OrganizationBase
from app.services.organization import get_organizations_by_activity_id, get_organizations_by_activity_id_deep

router = APIRouter(prefix="/activity", tags=["Activity"])


@router.get("/{activity_id}/organizations", response_model=List[OrganizationBase])
async def organizations_by_activity_id(activity_id: int, db: AsyncSession = Depends(get_db)):
    """Список организаций по коду вида деятельности"""
    return await get_organizations_by_activity_id(db, activity_id)


@router.get("/{activity_id}/organizations/deep", response_model=List[OrganizationBase])
async def organizations_by_activity_id_deep(activity_id: int, db: AsyncSession = Depends(get_db)):
    """Список организаций по коду вида деятельности (с вложенными категориями)"""
    return await get_organizations_by_activity_id_deep(db, activity_id)
