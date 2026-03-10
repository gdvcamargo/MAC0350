from pathlib import Path

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse, HTMLResponse

from requests.user_requests import UserInput
from models.user import User
from responses.user_response import UserResponse

app = FastAPI()

FILE_PATH = Path.cwd() / "files" / "index.html"

global USUARIOS
USUARIOS: list[User] = []


@app.get("/")
def index():
    content = ""
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content, status_code=status.HTTP_200_OK)


@app.post("/users")
def add_user(data: UserInput) -> JSONResponse:
    user = User(id=len(USUARIOS) + 1, nome=data.nome, idade=data.idade)
    USUARIOS.append(user)
    return JSONResponse(
        content={"message": "Usuário adicionado com sucesso"},
        status_code=status.HTTP_201_CREATED,
    )


@app.get("/users")
def get_users(index: int | None = None):
    if index:
        if index >= 0 and index < len(USUARIOS):
            user = USUARIOS[index]
            return UserResponse.from_user(user)
        return JSONResponse(content={"message": "Índice inválido"}, status_code=404)
    return [UserResponse.from_user(user) for user in USUARIOS]


@app.delete("/users")
def delete_users() -> JSONResponse:
    global USUARIOS
    USUARIOS = []
    content = {"message": "Usuários removidos com sucesso"}
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)
