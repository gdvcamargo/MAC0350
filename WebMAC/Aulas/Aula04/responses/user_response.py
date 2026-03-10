from pydantic import BaseModel
from models.user import User


class UserResponse(BaseModel):
    id: int
    nome: str
    idade: int

    @classmethod
    def from_user(cls, user: User):
        return UserResponse(
            id=user.id,
            nome=user.nome,
            idade=user.idade,
        )
