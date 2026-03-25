from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from db import SessionDep
from models.user_models import User
from repositories.user_repositories import UserSessionRepository


def authenticate_user(request: Request, session: SessionDep) -> User:
    token = request.cookies.get("session")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado"
        )
    user = UserSessionRepository.get_user_by_token(token=token, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sessão inválida ou expirada",
        )
    return user


def optional_authenticate_user(request: Request, session: SessionDep) -> User | None:
    token = request.cookies.get("session")
    if not token:
        return None
    user = UserSessionRepository.get_user_by_token(token=token, session=session)
    return user


AuthUser = Annotated[User, Depends(authenticate_user)]
LoggedUser = Annotated[User | None, Depends(optional_authenticate_user)]
