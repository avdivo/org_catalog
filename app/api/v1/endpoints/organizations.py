from typing import List
from fastapi import APIRouter
from app.schemas.schemas import OrganizationBase

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("/{organization_id}", response_model=OrganizationBase)
async def get_organization(organization_id: int):
    """Получить информацию об организации по её ID"""
    print(organization_id, '-----------')
    # return await get_organization(organization_id)
    pass


@router.get("/search", response_model=List[OrganizationBase])
async def search_organizations(name: str):
    """Поиск организаций по названию"""
    pass
