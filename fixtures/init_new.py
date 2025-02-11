import os
import json
import asyncio
from pathlib import Path
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import WKTElement

from app.core.database import async_session
from app.models.models import Building, Organization, PhoneNumber, Activity, organization_activity
from app.core.config import Config


async def insert_activities(session, data: dict, parent_id=None, path=""):
    """Рекурсивно вставляет данные из JSON в таблицу Activity."""
    for idx, (name, children) in enumerate(data.items(), start=1):
        new_path = f"{path}.{idx}" if path else str(idx)
        activity = Activity(name=name, parent_id=parent_id, path=new_path)
        session.add(activity)
        await session.flush()  # Получаем ID новой записи
        await insert_activities(session, children, activity.id, new_path)


async def load_data_from_json(session, json_file_path: str):
    """Добавляет данные из JSON в Organization, PhoneNumber, Building
    Возвращает словарь {organization_id: [activities_names]}}"""
    org_act = {}
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        building = Building(
            address=item['building']['address'],
            location=WKTElement(item['building']['location'], srid=4326)
        )
        session.add(building)
        await session.flush()

        organization = Organization(
            name=item['name'],
            building_id=building.id
        )
        session.add(organization)
        await session.flush()

        for phone in item['phone_numbers']:
            phone_number = PhoneNumber(
                number=phone['number'],
                organization_id=organization.id
            )
            session.add(phone_number)
            await session.flush()

        org_act[organization.id] = [a['name'] for a in item['activities']]

    return org_act


def create_links(session, org_act):
    """Добавляет организациям виды деятельности из словаря.
    Создает связи Organization с Activity"""
    for org in org_act.keys():
        stmt = select(Activity).filter(Activity.name.in_(org_act[org]))
        result = session.execute(stmt)  # Синхронный вызов
        activities = result.scalars().all()  # Получаем список всех активностей

        # 2. Получаем объект организации
        organization_stmt = select(Organization).filter(Organization.id == org)
        org_result = session.execute(organization_stmt)  # Синхронный вызов
        organization = org_result.scalar_one_or_none()  # Получаем одну организацию

        if organization is None:
            raise ValueError(f"Организация с id {org} не найдена.")

        # 4. Связываем каждый объект деятельности с организацией через промежуточную таблицу
        for activity in activities:
            organization.activities.append(activity)  # Добавляем связь


async def main():
    """ Основная логика: проверка наличия данных и их вставка. """

    print("Заполняем таблицу Activity...")
    DATA_FILE = Path(__file__).parent / "data" / "activities.json"
    with open(DATA_FILE, encoding="utf-8") as f:
        DATA = json.load(f)

    async with async_session() as session:
        await insert_activities(session, DATA)
        await session.commit()

    print("Заполняем таблицы...")
    async with async_session() as session:
        DATA_FILE = Path(__file__).parent / "data" / "organizations.json"
        org_act = await load_data_from_json(session, DATA_FILE)
        await session.commit()
        await session.close()

    print("Создание связей...")
    DATABASE_URL = (f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}"
                    f"@{os.getenv('DB_HOST', 'localhost')}:5432/{Config.DB_NAME}")
    engine = create_engine(DATABASE_URL, echo=True)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        create_links(session, org_act)
        session.commit()

    print("Инициализация данных завершена.")


if __name__ == "__main__":
    asyncio.run(main())
