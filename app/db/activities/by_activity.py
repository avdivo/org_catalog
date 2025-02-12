from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Activity

async def get_path_by_activity_id_from_db(db: AsyncSession, activity_id: int) -> str or None:
    """Запрос пути вида деятельности по его id"""
    async with (db.begin()):
        stmt = select(Activity.path).filter(Activity.id == activity_id)
        result = await db.execute(stmt)
        return result.scalar()