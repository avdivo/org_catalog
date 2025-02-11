import json
import asyncio
from pathlib import Path
from sqlalchemy import select
from geoalchemy2 import WKTElement
from app.models.models import Building, Organization, PhoneNumber, Activity
from app.core.database import get_db

async def load_data_from_json(json_file_path: str):
    # Чтение данных из JSON файла
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Получение сессии базы данных
    async for session in get_db():
        for item in data:
            # Создание объекта Building
            building = Building(
                address=item['building']['address'],
                location=WKTElement(item['building']['location'], srid=4326)
            )
            session.add(building)
            await session.flush()  # Сохраняем building, чтобы получить его ID

            # Создание объекта Organization
            organization = Organization(
                name=item['name'],
                building_id=building.id
            )
            session.add(organization)
            await session.flush()  # Сохраняем organization, чтобы получить его ID

            # Добавление телефонных номеров
            for phone in item['phone_numbers']:
                phone_number = PhoneNumber(
                    number=phone['number'],
                    organization_id=organization.id
                )
                session.add(phone_number)

            # Сопоставление с видами деятельности
            for activity_name in [a['name'] for a in item['activities']]:
                result = await session.execute(select(Activity).where(Activity.name == activity_name))
                activity = result.scalars().first()
                if activity:
                    organization.activities.append(activity)

        # Сохранение всех изменений в базе данных
        await session.commit()

async def main():
    # Укажите путь к вашему JSON файлу
    DATA_FILE = Path(__file__).parent / "data" / "organizations.json"
    await load_data_from_json(DATA_FILE)

# Запуск асинхронной функции
if __name__ == "__main__":
    asyncio.run(main())