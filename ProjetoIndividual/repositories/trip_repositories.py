from fastapi import HTTPException

from sqlmodel import Session, select

from models.trip_models import Trip, TripCreate, TripUpdate
from models.user_models import User


class TripRepository:
    @staticmethod
    def get_by_id(*, trip_id: int, session: Session) -> Trip | None:
        statement = select(Trip).where(Trip.id == trip_id)
        return session.exec(statement).first()

    @staticmethod
    def list_user_trips(*, user: User, session: Session) -> list[Trip]:
        statement = select(Trip).where(Trip.user_id == user.id)
        return list(session.exec(statement).all())

    @staticmethod
    def create_trip(*, user: User, input: TripCreate, session: Session) -> Trip:
        trip = Trip(
            user_id=user.id,
            name=input.name,
            destination=input.destination,
            start_date=input.start_date,
            end_date=input.end_date,
            budget=input.budget,
        )
        session.add(trip)
        session.commit()
        session.refresh(trip)
        return trip

    @staticmethod
    def get_user_trip_by_id(
        *, trip_id: int, user: User, session: Session
    ) -> Trip | None:
        statement = select(Trip).where(Trip.id == trip_id, Trip.user_id == user.id)
        return session.exec(statement).first()

    @staticmethod
    def update_trip(
        *,
        trip_id: int,
        user: User,
        input: TripUpdate,
        session: Session,
    ) -> Trip:
        trip = TripRepository.get_user_trip_by_id(
            trip_id=trip_id, user=user, session=session
        )
        if not trip:
            raise HTTPException(status_code=404, detail="Viagem não encontrada")

        trip.name = input.name
        trip.destination = input.destination
        trip.start_date = input.start_date
        trip.end_date = input.end_date
        trip.budget = input.budget
        session.add(trip)
        session.commit()
        session.refresh(trip)
        return trip

    @staticmethod
    def delete_trip(*, trip: Trip, session: Session) -> None:
        session.delete(trip)
        session.commit()
