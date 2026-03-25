from pathlib import Path

from fastapi.responses import JSONResponse

from fastapi import APIRouter, Depends, Request, Response
from fastapi.templating import Jinja2Templates

from db import SessionDep
from middlwares.auth_middlwares import AuthUser, authenticate_user
from models.trip_models import TripCreate, TripUpdate
from repositories.trip_repositories import TripRepository


router = APIRouter(
    prefix="/trips", tags=["Trips"], dependencies=[Depends(authenticate_user)]
)
templates = Jinja2Templates(directory=Path.cwd() / "templates")


@router.get("")
def trips_page(request: Request, user: AuthUser) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="trips/index.html",
        context={"logged_user": user},
    )


@router.get("/list")
def list_trips(request: Request, user: AuthUser, session: SessionDep) -> Response:
    trips = TripRepository.list_user_trips(user=user, session=session)
    return templates.TemplateResponse(
        request=request,
        name="trips/_list.html",
        context={"trips": trips},
    )


@router.post("/")
def create_trip(
    input: TripCreate,
    request: Request,
    user: AuthUser,
    session: SessionDep,
) -> Response:
    trip = TripRepository.create_trip(user=user, input=input, session=session)
    return templates.TemplateResponse(
        request=request,
        name="trips/_row.html",
        context={"trip": trip},
    )


@router.get("/{trip_id}")
def get_trip_row(
    trip_id: int, request: Request, user: AuthUser, session: SessionDep
) -> Response:
    trip = TripRepository.get_user_trip_by_id(
        trip_id=trip_id, user=user, session=session
    )
    if not trip:
        return Response(status_code=404)
    return templates.TemplateResponse(
        request=request,
        name="trips/_row.html",
        context={"trip": trip},
    )


@router.put("/{trip_id}")
def update_trip(
    trip_id: int,
    input: TripUpdate,
    request: Request,
    user: AuthUser,
    session: SessionDep,
) -> Response:
    trip = TripRepository.update_trip(
        trip_id=trip_id,
        user=user,
        input=input,
        session=session,
    )
    return templates.TemplateResponse(
        request=request,
        name="trips/_row.html",
        context={"trip": trip},
    )


@router.delete("/{trip_id}")
def delete_trip(
    trip_id: int,
    request: Request,
    user: AuthUser,
    session: SessionDep,
) -> Response:
    trip = TripRepository.get_user_trip_by_id(
        trip_id=trip_id, user=user, session=session
    )
    if not trip:
        return JSONResponse(
            status_code=404, content={"message": "Viagem não encontrada"}
        )
    TripRepository.delete_trip(trip=trip, session=session)
    return Response(status_code=204)
