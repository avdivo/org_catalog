import asyncio
import json
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import async_session
from app.models.models import Activity

# Читаем JSON-данные
DATA_FILE = Path(__file__).parent / "data" / "activities.json"
with open(DATA_FILE, encoding="utf-8") as f:
    DATA = json.load(f)


async def check_existing_data(session: AsyncSession) -> bool:
    """ Проверяет, есть ли уже данные в таблице Activity. """
    result = await session.execute(select(Activity).limit(1))
    return result.scalar() is not None


async def insert_activities(session: AsyncSession, data: dict, parent_id=None, path=""):
    """ Рекурсивно вставляет данные из JSON в таблицу Activity. """
    for idx, (name, children) in enumerate(data.items(), start=1):
        new_path = f"{path}.{idx}" if path else str(idx)
        activity = Activity(name=name, parent_id=parent_id, path=new_path)
        session.add(activity)
        await session.flush()  # Получаем ID новой записи
        await insert_activities(session, children, activity.id, new_path)


async def main():
    """ Основная логика: проверка наличия данных и их вставка. """
    async with async_session() as session:
        if await check_existing_data(session):
            print("Данные уже есть, пропускаем инициализацию.")
            return

        print("Заполняем таблицу Activity...")
        await insert_activities(session, DATA)
        await session.commit()
        print("Инициализация данных завершена.")


if __name__ == "__main__":
    asyncio.run(main())
