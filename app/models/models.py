from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from geoalchemy2 import Geometry
from typing import List, Optional

from app.core.database import Base


# Промежуточная таблица для связи Many-to-Many между Organization и Activity
organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", ForeignKey("organization.id"), primary_key=True),
    Column("activity_id", ForeignKey("activity.id"), primary_key=True)
)


class Building(Base):
    __tablename__ = "building"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    address: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[Geometry] = mapped_column(Geometry("POINT", srid=4326), nullable=False)

    organizations: Mapped[List["Organization"]] = relationship(back_populates="building")


class Activity(Base):
    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("activity.id"), nullable=True)
    path: Mapped[str] = mapped_column(nullable=False)  # Храним путь

    parent: Mapped[Optional["Activity"]] = relationship("Activity", remote_side=[id], backref="children")


class Organization(Base):
    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    building_id: Mapped[int] = mapped_column(ForeignKey("building.id"), nullable=False)

    building: Mapped["Building"] = relationship(back_populates="organizations")
    activities: Mapped[List["Activity"]] = relationship(secondary=organization_activity)
    phone_numbers: Mapped[List["PhoneNumber"]] = relationship(back_populates="organization")


class PhoneNumber(Base):
    __tablename__ = "phone_number"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String, nullable=False)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False)

    organization: Mapped["Organization"] = relationship(back_populates="phone_numbers")
