from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.trip_models import Trip


class UserSession(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    token: str = Field(index=True, unique=True)
    expires_at: datetime


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    username_display: str
    password: str
    name: str

    trips: list["Trip"] = Relationship(back_populates="user")


class UserCreate(BaseModel):
    username: str
    password: str
    name: str


class UserLogin(BaseModel):
    username: str
    password: str
