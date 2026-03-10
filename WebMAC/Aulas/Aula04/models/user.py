from pydantic import BaseModel


class User(BaseModel):
    id: int
    nome: str
    idade: int
