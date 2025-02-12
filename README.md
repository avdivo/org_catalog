# Каталог организаций

```plaintext
org_catalog/
├── alembic/                     # Каталог миграций Alembic
│   ├── versions/                # Каталог с версиями миграций
│   ├── env.py                   # Конфигурация Alembic
│   ├── script.py.mako           # Шаблон для генерации новых миграций
│
├── app/                         # Основной код FastAPI-приложения
│   ├── main.py                  # Главный вход в приложение
│   ├── __init__.py              # Инициализация пакета
│   │
│   ├── api/                     # API-роутеры
│   │   ├── __init__.py          # Инициализация пакета
│   │   ├── v1/                  # Версия API (можно расширять `v2`, `v3` и т. д.)
│   │   │   ├── __init__.py      # Инициализация пакета
│   │   │   ├── endpoints/       # Каталог с эндпоинтами
│   │   │   │   ├── __init__.py  # Инициализация пакета
│   │   │   │   ├── items.py     # Роутер для работы с товарами
│   │   │   │   ├── users.py     # Роутер для работы с пользователями
│   │
│   ├── core/                    # Основные настройки приложения
│   │   ├── __init__.py          # Инициализация пакета
│   │   ├── config.py            # Конфигурация FastAPI (настройки, переменные окружения)
│   │   ├── database.py          # Подключение к базе данных PostgreSQL
│   │   ├── security.py          # Аутентификация и авторизация (OAuth, JWT)
│   │
│   ├── crud/                    # CRUD-операции с БД
│   │   ├── __init__.py          # Инициализация пакета
│   │   ├── base.py              # Базовые операции CRUD
│   │   ├── item.py              # CRUD для товаров
│   │   ├── user.py              # CRUD для пользователей
│   │
│   ├── models/                  # SQLAlchemy модели БД
│   │   ├── __init__.py          # Инициализация пакета
│   │   ├── base.py              # Базовая модель SQLAlchemy
│   │   ├── item.py              # Модель товаров
│   │   ├── user.py              # Модель пользователей
│   │
│   ├── schemas/                 # Pydantic-схемы для валидации данных
│   │   ├── __init__.py          # Инициализация пакета
│   │   ├── item.py              # Схемы для товаров
│   │   ├── user.py              # Схемы для пользователей
│   │
│   ├── services/                # Бизнес-логика приложения
│   │   ├── __init__.py          # Инициализация пакета
│   │   ├── item_service.py      # Сервис для товаров
│   │   ├── user_service.py      # Сервис для пользователей
│
├── migrations/                  # Скрипты для начального заполнения БД
│   ├── seed_data.py             # Скрипт для заполнения справочников
│
├── tests/                       # Тесты (pytest)
│   ├── __init__.py              # Инициализация пакета
│   ├── test_items.py            # Тесты для товаров
│   ├── test_users.py            # Тесты для пользователей
│
│── .env                        # Переменные окружения (настройки БД, секретные ключи)
│── Dockerfile                  # Docker-образ для FastAPI
│── docker-compose.yml           # Композиция контейнеров (FastAPI + PostgreSQL/PostGIS)
│── requirements.txt             # Список зависимостей Python
│── alembic.ini                  # Конфигурационный файл Alembic
│── README.md                    # Документация по проекту
```



Миграция для создания таблиц исправлена вручную.  
Добавлен:  
import geoalchemy2  

Закомментировано:  
    # op.drop_table('spatial_ref_sys')  
    # op.create_index('idx_building_location', 'building', ['location'], unique=False, postgresql_using='gist')  
    # op.drop_index('idx_building_location', table_name='building', postgresql_using='gist')  


Запуск:  
    docker compose up -d db  
    alembic upgrade head  
    python init_db.py  

    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Остановить БД и очистить:  
    docker compose up -d db


