"""Database configuration and session utilities for the FastAPI app."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/blog_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Provide a SQLAlchemy session for request handling and close it safely."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
