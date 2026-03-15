from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import get_settings

settings = get_settings()

DEFAULT_SQLITE_URL = "sqlite:///task_optimizer.db"


def _build_engine(database_url: str):
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    return create_engine(database_url, pool_pre_ping=True, connect_args=connect_args)


def _create_engine_with_fallback(primary_url: str):
    primary_engine = _build_engine(primary_url)
    try:
        with primary_engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return primary_engine, primary_url
    except SQLAlchemyError:
        fallback_engine = _build_engine(DEFAULT_SQLITE_URL)
        with fallback_engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return fallback_engine, DEFAULT_SQLITE_URL


engine, active_database_url = _create_engine_with_fallback(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
