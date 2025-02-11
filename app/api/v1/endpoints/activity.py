from typing import List
from fastapi import APIRouter
from app.schemas.schemas import OrganizationBase

router = APIRouter(prefix="/activity", tags=["Activity"])


@router.get("/{activity_id}/organizations", response_model=List[OrganizationBase])
async def get_organizations_by_activity(activity_id: int):
    """Список организаций по виду деятельности"""
    pass


@router.get("/{activity_id}/organizations/deep", response_model=List[OrganizationBase])
async def get_organizations_by_activity_deep(activity_id: int):
    """Список организаций по виду деятельности (с вложенными категориями)"""
    pass
