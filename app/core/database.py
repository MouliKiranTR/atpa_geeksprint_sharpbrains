"""
Database configuration and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings

# Create database engine
database_url = settings.DATABASE_URL or "sqlite:///./app.db"
engine = create_engine(
    database_url,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_pre_ping=True,   # Verify connections before use
    pool_recycle=3600     # Recycle connections every hour
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all database tables
    """
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """
    Drop all database tables (useful for testing)
    """
    Base.metadata.drop_all(bind=engine) 