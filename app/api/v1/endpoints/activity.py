from typing import List
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from .docs import Docs
from app.core.database import get_db
from app.schemas.schemas import OrganizationBase
from app.services.organization import get_organizations_by_activity_id, get_organizations_by_activity_id_deep

router = APIRouter(prefix="/activity", tags=["Activity"])


@router.get("/{activity_id}/organizations", **Docs.ACT_ID, response_model=List[OrganizationBase])
async def organizations_by_activity_id(
        activity_id: int = Path(..., description="Код деятельности"),
        db: AsyncSession = Depends(get_db)):
    """Список организаций по коду вида деятельности"""
    return await get_organizations_by_activity_id(db, activity_id)


@router.get("/{activity_id}/organizations/deep", **Docs.ACT_DEEP, response_model=List[OrganizationBase])
async def organizations_by_activity_id_deep(
        activity_id: int = Path(..., description="Код деятельности"),
        db: AsyncSession = Depends(get_db)):
    """Список организаций по коду вида деятельности (с вложенными категориями)"""
    return await get_organizations_by_activity_id_deep(db, activity_id)
