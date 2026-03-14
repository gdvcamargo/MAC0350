from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    password: str
    bio: str


class UserCreate(BaseModel):
    name: str
    password: str
    bio: str


class UserLogin(BaseModel):
    name: str
    password: str
