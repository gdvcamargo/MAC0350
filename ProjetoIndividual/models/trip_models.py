from datetime import date
from typing import TYPE_CHECKING
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from models.user_models import User


class Trip(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str
    destination: str
    start_date: date
    end_date: date
    budget: float

    user: "User" = Relationship(back_populates="trips")


class TripCreate(BaseModel):
    name: str
    destination: str
    start_date: date
    end_date: date
    budget: float


class TripUpdate(TripCreate):
    pass
