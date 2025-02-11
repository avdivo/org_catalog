from pydantic import BaseModel, field_validator
from typing import List, Optional
from shapely.geometry import Point


# Схема для отображения данных о здании
class BuildingBase(BaseModel):
    id: int
    address: str
    location: str  # Тип изменим на строку, чтобы хранить координаты

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    # Валидатор для поля location
    @field_validator('location')
    def convert_location(cls, value):
        # Преобразуем объект Geometry в строку с координатами
        if isinstance(value, Point):
            latitude = value.y  # Широта
            longitude = value.x  # Долгота
            return f"Широта: {latitude}, Долгота: {longitude}"
        return value  # Если это не Point, просто возвращаем значение как есть


# Схема для отображения данных об активности
class ActivityBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# Схема для отображения данных о телефонном номере
class PhoneNumberBase(BaseModel):
    id: int
    number: str

    class Config:
        from_attributes = True


# Схема для отображения организации
class OrganizationBase(BaseModel):
    id: int
    name: str
    building: BuildingBase
    activities: List[ActivityBase]
    phone_numbers: List[PhoneNumberBase]

    class Config:
        from_attributes = True
