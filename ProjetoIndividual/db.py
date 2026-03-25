from collections.abc import Generator
from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

from models import (  # noqa: F401
    user_models,
    trip_models,
)


DATABASE_NAME = "projeto-webmac.db"
DATABASE_URL = f"sqlite:///{DATABASE_NAME}"

engine = create_engine(DATABASE_URL)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def create_tables() -> None:
    SQLModel.metadata.create_all(engine)


SessionDep = Annotated[Session, Depends(get_db)]
