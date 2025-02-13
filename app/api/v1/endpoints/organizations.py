from typing import List
from fastapi import APIRouter, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .docs import Docs
from app.core.database import get_db
from app.core.security import verify_api_key
from app.schemas.schemas import OrganizationBase
from app.services.organization import get_organization_by_id, search_organization_by_name

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("/{organization_id}", **Docs.GET_ORG, response_model=OrganizationBase)
async def get_organization(
        auth: bool = Depends(verify_api_key),
        organization_id: int = Path(..., description="Идентификатор организации"),
        db: AsyncSession = Depends(get_db)):
    """Получить информацию об организации по её ID"""
    return await get_organization_by_id(db, organization_id)


@router.get("/search/", **Docs.SEARCH_ORG, response_model=List[OrganizationBase])
async def search_organizations(
        auth: bool = Depends(verify_api_key),
        organization_name: str = Path(..., description="Название или его часть"),
        db: AsyncSession = Depends(get_db)):
    """Поиск организаций по названию"""
    return await search_organization_by_name(db, organization_name)
