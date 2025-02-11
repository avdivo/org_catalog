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
        json_schema_extra = {
            "example": {
                "id": 1,
                "address": "ул. Пушкина, д. 1",
                "location": "POINT(37.6176 55.7558)",
                "location_text": "Широта: 55.7558, Долгота: 37.6176"
            }
        }

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
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Производственная деятельность"
            }
        }


# Схема для отображения данных о телефонном номере
class PhoneNumberBase(BaseModel):
    id: int
    number: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "number": "+7 123 456 78 90"
            }
        }


# Схема для отображения организации
class OrganizationBase(BaseModel):
    id: int
    name: str
    building: BuildingBase
    activities: List[ActivityBase]
    phone_numbers: List[PhoneNumberBase]

    class Config:
        from_attributes = True
        # json_schema_extra1 = {
        #     "example": {
        #         "id": 1,
        #         "name": "ООО 'Пример'",
        #         "building": {
        #             "id": 1,
        #             "address": "ул. Пушкина, д. 1",
        #             "location": "POINT(37.6176 55.7558)"
        #         },
        #         "activities": [
        #             {
        #                 "id": 1,
        #                 "name": "Производственная деятельность"
        #             }
        #         ],
        #         "phone_numbers": [
        #             {
        #                 "id": 1,
        #                 "number": "+7 123 456 78 90"
        #             }
        #         ]
        #     }
        # }
