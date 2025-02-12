from typing import List
from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.schemas import OrganizationBase
from app.services.organization import get_organization_by_id, search_organization_by_name

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("/{organization_id}", response_model=OrganizationBase)
async def get_organization(organization_id: int, db: AsyncSession = Depends(get_db)):
    """Получить информацию об организации по её ID"""
    return await get_organization_by_id(db, organization_id)


@router.get("/search/", response_model=List[OrganizationBase])
async def search_organizations(organization_name: str = Query(...), db: AsyncSession = Depends(get_db)):
    """Поиск организаций по названию"""
    return await search_organization_by_name(db, organization_name)
