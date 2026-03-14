import hashlib

from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Depends, Cookie, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from models.user_models import User, UserCreate, UserLogin


FILE_PATH = Path.cwd() / "files" / "index.html"
STATIC_FILES_PATH = Path.cwd() / "static"
TEMPLATES_FILES_PATH = Path.cwd() / "templates"

USUARIOS: list[User] = []

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_FILES_PATH), name="static")
templates = Jinja2Templates(directory=TEMPLATES_FILES_PATH)


def get_current_user(sessionId: Annotated[str | None, Cookie()] = None) -> User | None:
    if not sessionId:
        return None

    user = next((user for user in USUARIOS if user.id == sessionId), None)
    return user


CurrentUser = Annotated[User | None, Depends(get_current_user)]


@app.get("/")
def sign_up_page(request: Request, logged_user: CurrentUser):
    return templates.TemplateResponse(
        request=request, name="sign-up.html", context={"logged_user": logged_user}
    )


@app.post("/sign-up")
def sign_up_user(input: UserCreate) -> JSONResponse:
    hashed_password = hashlib.sha256(input.password.encode()).hexdigest()
    user_id_str = input.name + input.password
    user_id = hashlib.sha256(user_id_str.encode()).hexdigest()
    user = User(id=user_id, name=input.name, password=hashed_password, bio=input.bio)
    USUARIOS.append(user)

    response = JSONResponse(
        content={"message": "Usuário adicionado com sucesso"},
        status_code=status.HTTP_201_CREATED,
    )
    response.set_cookie(key="sessionId", value=user_id, httponly=True)
    return response


@app.get("/sign-in")
def sign_in_page(request: Request, logged_user: CurrentUser):
    return templates.TemplateResponse(
        "sign-in.html", request=request, context={"logged_user": logged_user}
    )


@app.post("/sign-in")
def sign_in_user(input: UserLogin) -> JSONResponse:
    hashed_password = hashlib.sha256(input.password.encode()).hexdigest()
    for user in USUARIOS:
        if user.name == input.name and user.password == hashed_password:
            response = JSONResponse(
                content={"message": "Login bem-sucedido"},
                status_code=status.HTTP_200_OK,
            )
            response.set_cookie(key="sessionId", value=user.id, httponly=True)
            return response
    return JSONResponse(
        content={"message": "Credenciais inválidas"},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


@app.get("/home")
def home_page(request: Request, logged_user: CurrentUser):
    if not logged_user:
        context = {}
        return templates.TemplateResponse(
            request=request, name="page_401.html", context=context
        )

    context = {"logged_user": logged_user.model_dump()}
    return templates.TemplateResponse(
        request=request, name="profile.html", context=context
    )
