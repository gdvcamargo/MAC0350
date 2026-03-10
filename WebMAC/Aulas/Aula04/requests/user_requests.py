from pydantic import BaseModel


class UserInput(BaseModel):
    nome: str
    idade: int
