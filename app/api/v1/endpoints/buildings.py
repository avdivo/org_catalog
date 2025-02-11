from typing import List
from fastapi import APIRouter
from app.schemas.schemas import OrganizationBase

router = APIRouter(prefix="/buildings", tags=["Buildings"])


@router.get("/{building_id}/organizations", response_model=List[OrganizationBase])
async def get_organizations_in_building(building_id: int):
    """Список организаций в конкретном здании"""
    pass
