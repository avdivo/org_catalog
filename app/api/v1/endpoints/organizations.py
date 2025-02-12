from typing import List
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.core.database import get_db
from app.schemas.schemas import OrganizationBase
from app.db.crud import get_organization_by_id

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("/{organization_id}", response_model=OrganizationBase)
async def get_organization(organization_id: int, db: AsyncSession = Depends(get_db)):
    """Получить информацию об организации по её ID"""
    return await get_organization_by_id(db, organization_id)


@router.get("/search", response_model=List[OrganizationBase])
async def search_organizations(name: str):
    """Поиск организаций по названию"""
    pass
