from pathlib import Path

from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from db import SessionDep
from middlwares.auth_middlwares import LoggedUser
from models.user_models import UserCreate, UserLogin
from repositories.user_repositories import UserRepository, UserSessionRepository
from utils import must_be_int, verify_password

router = APIRouter(prefix="/users", tags=["Users"], dependencies=[])
templates = Jinja2Templates(directory=Path.cwd() / "templates")


@router.get("/register")
def register_page(request: Request, logged_user: LoggedUser) -> Response:
    if logged_user:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse(
        request=request,
        name="/users/register.html",
        context={"logged_user": None},
    )


@router.post("/register")
async def create_user(
    input: UserCreate, session: SessionDep, response: Response
) -> JSONResponse:
    user = UserRepository.create_user(input=input, session=session)
    user_session = UserSessionRepository.create_session(
        user_id=must_be_int(user.id), session=session
    )
    response = JSONResponse(content={"message": "Usuário criado com sucesso"})
    response.set_cookie(
        key="session",
        value=user_session.token,
        httponly=True,
        expires=int(user_session.expires_at.timestamp()),
    )
    return response


@router.get("/login")
def login_page(request: Request, logged_user: LoggedUser) -> Response:
    if logged_user:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse(
        request=request,
        name="/users/login.html",
        context={"logged_user": None},
    )


@router.post("/login")
def login_user(
    input: UserLogin, session: SessionDep, response: Response
) -> JSONResponse:
    user = UserRepository.get_user_by_username(username=input.username, session=session)
    if not user:
        return JSONResponse(
            content={"message": "Credenciais inválidas"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    if not verify_password(password=input.password, hashed_password=user.password):
        return JSONResponse(
            content={"message": "Credenciais inválidas"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    user_session = UserSessionRepository.refresh_user_session(
        user_id=must_be_int(user.id), session=session
    )
    response = JSONResponse(content={"message": f"Bem vindo, {user.name}!"})
    response.set_cookie(
        key="session",
        value=user_session.token,
        httponly=True,
        expires=int(user_session.expires_at.timestamp()),
    )
    return response


@router.get("/logout")
def logout_user(
    response: Response, logged_user: LoggedUser, session: SessionDep
) -> JSONResponse:
    if not logged_user:
        return JSONResponse(
            content={"message": "Usuário não autenticado"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    UserSessionRepository.delete_session(
        token=logged_user.session_token, session=session
    )
    response = JSONResponse(content={"message": "Logout realizado com sucesso"})
    response.delete_cookie(key="session")
    return response
