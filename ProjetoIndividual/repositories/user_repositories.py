from fastapi import HTTPException, status
from sqlmodel import Session, select
from datetime import datetime, timedelta

from models.user_models import User, UserCreate, UserSession
from utils import generate_rand_token, hash_password


class UserSessionRepository:
    @staticmethod
    def create_session(*, user_id: int, session: Session) -> UserSession:
        expires_at = datetime.now() + timedelta(days=7)
        token = generate_rand_token()
        user_session = UserSession(user_id=user_id, token=token, expires_at=expires_at)
        session.add(user_session)
        session.commit()
        session.refresh(user_session)
        return user_session

    @staticmethod
    def get_session_by_token(*, token: str, session: Session) -> UserSession | None:
        statement = select(UserSession).where(UserSession.token == token)
        return session.exec(statement).first()

    @staticmethod
    def get_user_by_token(*, token: str, session: Session) -> User | None:
        statement = select(UserSession).where(UserSession.token == token)
        user_session = session.exec(statement).first()
        if not user_session:
            return None

        if user_session.expires_at < datetime.now():
            session.delete(user_session)
            session.commit()
            return None

        user_statement = select(User).where(User.id == user_session.user_id)
        return session.exec(user_statement).first()

    @staticmethod
    def refresh_user_session(*, user_id: int, session: Session) -> UserSession:
        statement = select(UserSession).where(UserSession.user_id == user_id)
        user_session = session.exec(statement).first()
        if not user_session:
            return UserSessionRepository.create_session(
                user_id=user_id, session=session
            )

        user_session.expires_at = datetime.now() + timedelta(days=7)
        session.add(user_session)
        session.commit()
        session.refresh(user_session)
        return user_session

    @staticmethod
    def delete_session(*, id: int, session: Session) -> None:
        statement = select(UserSession).where(UserSession.id == id)
        user_session = session.exec(statement).first()
        if user_session:
            session.delete(user_session)
            session.commit()


class UserRepository:
    @staticmethod
    def check_username_exists(*, username: str, session: Session) -> bool:
        statement = select(User).where(User.username == username)
        return session.exec(statement).first() is not None

    @staticmethod
    def create_user(*, input: UserCreate, session: Session) -> User:
        if UserRepository.check_username_exists(
            username=input.username.lower(), session=session
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao criar usuário",
            )

        user = User(
            username=input.username.lower(),
            username_display=input.username,
            password=hash_password(input.password),
            name=input.name,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def get_user_by_id(*, user_id: int, session: Session) -> User | None:
        statement = select(User).where(User.id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def get_user_by_username(*, username: str, session: Session) -> User | None:
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()
