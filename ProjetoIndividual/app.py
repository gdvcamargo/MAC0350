from pathlib import Path
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from middlwares.auth_middlwares import LoggedUser
from routes.trip_routes import router as TripRouter
from routes.user_routes import router as UserRouter

FILE_PATH = Path.cwd() / "files" / "index.html"
STATIC_FILES_PATH = Path.cwd() / "static"
TEMPLATES_FILES_PATH = Path.cwd() / "templates"

app = FastAPI(title="Projeto Individual WebMAC")


app.mount("/static", StaticFiles(directory=STATIC_FILES_PATH), name="static")
templates = Jinja2Templates(directory=TEMPLATES_FILES_PATH)

app.include_router(UserRouter)
app.include_router(TripRouter)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> Response:
    if exc.status_code == 401:
        if request.headers.get("HX-Request") == "true":
            response = Response(status_code=401)
            response.headers["HX-Redirect"] = "/users/login"
            return response

        accept_header = request.headers.get("accept", "")
        if "text/html" in accept_header or request.method == "GET":
            return RedirectResponse(url="/users/login", status_code=302)

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers,
    )


@app.get("/")
def home_page(request: Request, logged_user: LoggedUser) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="/index.html",
        context={"logged_user": logged_user},
    )


@app.get("/home")
def home_alias_page(request: Request, logged_user: LoggedUser) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="/index.html",
        context={"logged_user": logged_user},
    )
