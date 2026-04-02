"""
    Defines the database module.
    
    Parameters:
    None (None): This module does not accept parameters.
    
    Returns:
    None: This module does not return a value.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/blog_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
        Handles the get db operation.
        
        Parameters:
        None (None): This function does not require parameters.
        
        Returns:
        Any: The result produced by this function.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
