# Каталог организаций


[**Swagger**](https://328c22e35a29.vps.myjino.ru/docs): https://328c22e35a29.vps.myjino.ru/docs  
[GitHub](https://github.com/avdivo/org_catalog): https://github.com/avdivo/org_catalog


## Описание
Сервис для получения информации об организациях по API

## Функции
- вывод информации об организации по её идентификатору
- поиск организации по названию
- список всех организаций, которые относятся к указанному виду деятельности
- искать организации по виду деятельности. Например, поиск по виду деятельности «Еда», которая находится на первом уровне дерева, и чтобы нашлись все организации, которые относятся к видам деятельности, лежащим внутри. Т.е. в результатах поиска должны отобразиться организации с видом деятельности Еда, Мясная продукция, Молочная продукция.
- список организаций, которые находятся в заданном радиусе (по координатам на карте и радиусу)
- список организаций, которые находятся в заданноq прямоугольной области (по координатам на карте 2 точек)
- список всех организаций находящихся в конкретном здании

## Структура проекта

```plaintext
org_catalog/
├── alembic/                     # Каталог миграций Alembic
├── app/                         # Основной код приложения
│   ├── api/                     # API-интерфейс
│   │   ├── v1/                  # Версия API v1
│   │   │   ├── endpoints/       # Обработчики API
│   │   │   │   ├── __init__.py
│   │   │   │   ├── activity.py
│   │   │   │   ├── buildings.py
│   │   │   │   ├── docs.py
│   │   │   │   ├── error.py
│   │   │   │   ├── geo.py
│   │   │   │   ├── organizations.py
│   │   │   ├── __init__.py
│   │   ├── __init__.py
│   ├── core/                    # Базовые настройки и утилиты
│   │   ├── __init__.py
│   │   ├── config.py             # Конфигурация приложения
│   │   ├── database.py           # Настройки базы данных
│   │   ├── security.py           # Безопасность и аутентификация
│   ├── db/                       # Работа с базой данных
│   │   ├── activities/
│   │   │   ├── __init__.py
│   │   │   ├── by_activity.py    # Запросы по видам деятельности
│   │   ├── organizations/        # Запросы по организациям
│   │   │   ├── __init__.py
│   │   │   ├── by_activity.py
│   │   │   ├── by_building.py
│   │   │   ├── by_geo.py
│   │   │   ├── by_organization.py
│   ├── models/                   # Описание моделей БД
│   │   ├── __init__.py
│   │   ├── models.py
│   ├── schemas/                  # Схемы для валидации данных (Pydantic)
│   │   ├── __init__.py
│   │   ├── schemas.py
│   ├── services/                 # Бизнес-логика приложения
│   │   ├── __init__.py
│   │   ├── organization.py        # Логика работы с организациями
│   ├── main.py                    # Основной вход в приложение
├── fixtures/                      # Тестовые данные
│   ├── activities.json            # Виды деятельности
│   ├── organizations.json         # Организации
├── init-scripts/                  # Скрипты инициализации
│   ├── init-postgis.sql           # Скрипт для инициализации PostGIS
├── tests/                         # Тесты проекта
├── venv/                          # Виртуальное окружение (не входит в репозиторий)
├── .dockerignore                  # Игнорируемые файлы для Docker
├── .env                            # Переменные окружения
├── .env_server                     # Переменные окружения для сервера
├── alembic.ini                     # Конфигурация Alembic
├── docker-compose.yml              # Конфигурация Docker Compose
├── Dockerfile                      # Конфигурация Docker-контейнера
├── init_db.py                      # Скрипт инициализации БД
├── README.md                        # Документация
├── requirements.txt                 # Список зависимостей
```

## Используемые зависимости
fastapi==0.115.2  
uvicorn==0.34.0  
SQLAlchemy==2.0.37  
GeoAlchemy2==0.17.0  
asyncpg==0.30.0  
alembic==1.14.1  
python-dotenv==1.0.1  
psycopg2-binary==2.9.10  
shapely==2.0.7  

## Файл .env
DB_NAME=<Имя БД>  
DB_USER=<Пользователь БД>  
DB_PASSWORD=<Пароль БД>  
APP_PORTS=8000:8000 <Внешний и внутренний порты контейнера. Без контейнера запускается на внутреннем>  
API_KEY=<Статический ключ для авторизации> (YXZkaXZv)

Файл нужно поместить в корень проекта, папку org_catalog.  
При запуске на сервере внешний порт контейнера можно указать другой:  
APP_PORTS=80:8000  


## Установка и запуск в Docker контейнере
1. Открыть терминал.
2. Перейти в папку, где будет проект.
3. Клонировать репозиторий:
    ```bash
    git clone https://github.com/avdivo/org_catalog
    ```
4. Войти в папку проекта.
    ```bash
    cd org_catalog
    ```
   > Не забыть поместить или создать в папке файл .env
5. Запустить PostgtesSQL + PostGIS в контейнере
    ```bash
    docker compose up -d db 
    ```
   > Автоматически создастся БД и в ней активируется PostGIS

6. Создать и активировать виртуальное окружение
    ```bash
    python3 -m venv venv
    source venv/bin/activate 
    ```
   и установить зависимости
   ```bash
    pip install -r requirements.txt 
   ```
7. Выполнить миграции Alembic
    ```bash
    alembic upgrade head 
    ```
8. Заполнить БД тестовыми данными
    ```bash
    python init_db.py
    ```
9. Запустить проект в контейнере
    ```bash
    docker compose up -d
    ```
10. Остановить проект и удалить БД:
    ```bash
    docker compose down -v  # Без -v БД не удаляется
    ```
11. Запустить проект повторно (если БД существует)
    ```bash
    docker compose up --build
    ```

## Для запуска без контейнера
После п.8 (если БД будет в контейнере) можно запустить проект:  
```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload >> /home/$USER/uvicorn.log 2>&1
```
```
python -m app.main
```

## Использование
Для вызова эндпоинтов API требуется авторизация. Передавайте ключ X-API-KEY в заголовке запроса со значением YXZkaXZv.
```bash

curl -X 'GET' \
  'https://328c22e35a29.vps.myjino.ru/api/v1/organizations/1' \
  -H 'accept: application/json' \
  -H 'X-API-KEY: YXZkaXZv'
```
https://328c22e35a29.vps.myjino.ru/api/v1/organizations/1
```
Возвращает детальную информацию об организации по её уникальному идентификатору.
```



```bash
curl -X 'GET' \
  'https://328c22e35a29.vps.myjino.ru/api/v1/organizations/search/?organization_name=%D0%90%D0%B2%D1%82%D0%BE%D0%9C%D0%B8%D1%80' \
  -H 'accept: application/json' \
  -H 'X-API-KEY: YXZkaXZv'
```
https://328c22e35a29.vps.myjino.ru/api/v1/organizations/search/?organization_name=АвтоМир
```
Позволяет искать организации по частичному или полному названию.
```

```bash
curl -X 'GET' \
  'https://328c22e35a29.vps.myjino.ru/api/v1/activity/2/organizations' \
  -H 'accept: application/json' \
  -H 'X-API-KEY: YXZkaXZv'
```
https://328c22e35a29.vps.myjino.ru/api/v1/activity/2/organizations
```
Возвращает список организаций, относящихся к указанному виду деятельности.
```

```bash
curl -X 'GET' \
  'https://328c22e35a29.vps.myjino.ru/api/v1/activity/35/organizations/deep' \
  -H 'accept: application/json' \
  -H 'X-API-KEY: YXZkaXZv'
```
https://328c22e35a29.vps.myjino.ru/api/v1/activity/35/organizations/deep
```
Возвращает список организаций, относящихся к указанному виду деятельности, а также ко всем его вложенным категориям.
```

```bash
curl -X 'GET' \
  'https://328c22e35a29.vps.myjino.ru/api/v1/geo/radius?lat=55.819&lon=37.53&radius=10' \
  -H 'accept: application/json' \
  -H 'X-API-KEY: YXZkaXZv'
```
https://328c22e35a29.vps.myjino.ru/api/v1/geo/radius?lat=55.819&lon=37.53&radius=10
```
Возвращает список организаций, расположенных в пределах заданного радиуса относительно указанной точки на карте.
```

```bash
curl -X 'GET' \
  'https://328c22e35a29.vps.myjino.ru/api/v1/geo/rectangle?top_left_lat=55.81&top_left_lon=37.51&bottom_right_lat=55.9&bottom_right_lon=37.55' \
  -H 'accept: application/json' \
  -H 'X-API-KEY: YXZkaXZv'
```
https://328c22e35a29.vps.myjino.ru/api/v1/geo/rectangle?top_left_lat=55.81&top_left_lon=37.51&bottom_right_lat=55.9&bottom_right_lon=37.55
```
Возвращает список организаций, находящихся в пределах заданной прямоугольной области, определенной координатами верхнего левого и нижнего правого углов.
```

```bash
curl -X 'GET' \
  'https://328c22e35a29.vps.myjino.ru/api/v1/buildings/5/organizations' \
  -H 'accept: application/json' \
  -H 'X-API-KEY: YXZkaXZv'
```
https://328c22e35a29.vps.myjino.ru/api/v1/buildings/5/organizations
```
Возвращает список всех организаций, находящихся в указанном здании.
```



## Тестирование
Для запуска основных тестов нужно запустить тестирование
```
pytests tests/
```

## Миграции
После создания миграции в ней закомментированы строки вызывающие ошибки
- op.drop_table('spatial_ref_sys')  
- op.create_index('idx_building_location', 'building', ['location'], unique=False, postgresql_using='gist')  
- op.drop_index('idx_building_location', table_name='building', postgresql_using='gist')  
