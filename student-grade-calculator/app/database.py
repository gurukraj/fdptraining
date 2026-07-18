"""
Database configuration module.

Sets up the SQLAlchemy engine, session factory, and base class for models.
Uses SQLite as the database backend for zero-configuration setup.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Database URL - defaults to a local SQLite file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./grades.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


def get_db():
    """
    Dependency that provides a database session.

    Yields a SQLAlchemy session and ensures it is closed after use.
    Used as a FastAPI dependency injection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
