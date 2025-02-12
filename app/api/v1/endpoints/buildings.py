from typing import List
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from .docs import Docs
from app.core.database import get_db
from app.schemas.schemas import OrganizationBase
from app.services.organization import get_organizations_in_building

router = APIRouter(prefix="/buildings", tags=["Buildings"])


@router.get("/{building_id}/organizations", **Docs.BUILDING, response_model=List[OrganizationBase])
async def organizations_in_building(
        building_id: int = Path(..., description="Идентификатор здания"),
        db: AsyncSession = Depends(get_db)):
    """Список организаций в конкретном здании"""
    return await get_organizations_in_building(db, building_id)
