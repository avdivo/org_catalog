import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    APP_PORTS = os.getenv('APP_PORTS')[-4:]
    API_KEY = os.getenv('API_KEY')
