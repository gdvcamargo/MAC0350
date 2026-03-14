from pydantic import BaseModel
from models.user_models import User


class UserResponse(BaseModel):
    id: int
    name: str
    password: str
    bio: str

    @classmethod
    def from_user(cls, user: User):
        return UserResponse(
            id=user.id,
            name=user.name,
            password=user.password,
            bio=user.bio,
        )
