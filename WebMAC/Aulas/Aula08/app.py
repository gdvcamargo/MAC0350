from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory=Path.cwd())

LIKES = 0


def render_home(request: Request, aba_ativa: str):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"curtidas": LIKES, "aba_ativa": aba_ativa},
    )


@app.get("/")
def root(request: Request):
    return render_home(request, "curtidas")


@app.get("/home")
def home(request: Request):
    return render_home(request, "curtidas")


@app.get("/home/curtidas")
def home_curtidas(request: Request):
    return render_home(request, "curtidas")


@app.get("/home/jupiter")
def home_jupiter(request: Request):
    return render_home(request, "jupiter")


@app.get("/home/professor")
def home_professor(request: Request):
    return render_home(request, "professor")


@app.post("/curtir")
def curtir():
    global LIKES
    LIKES += 1

    return HTMLResponse(content=f'<strong id="likes-count">Curtidas: {LIKES}</strong>')


@app.delete("/curtir")
def apagar_curtidas():
    global LIKES
    LIKES = 0

    return HTMLResponse(content=f'<strong id="likes-count">Curtidas: {LIKES}</strong>')


@app.get("/likes")
def get_likes():
    return {"likes": LIKES}
