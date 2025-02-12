from pydantic import BaseModel, field_validator
from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKBElement
from typing import List, Optional
from shapely.geometry import Point


# Схема для отображения данных о здании
class BuildingBase(BaseModel):
    id: int
    address: str
    location: list[float]  # Тип изменим на строку, чтобы хранить координаты

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


    @field_validator('location', mode='before')
    def convert_location(cls, value):
        """Конвертирует WKBElement → Point → строку с координатами"""
        if isinstance(value, WKBElement):  # Если объект типа WKBElement
            value = to_shape(value)  # Конвертируем в объект Point
            value = [value.y, value.x]
        return value

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
