"""
    Defines the database module.
    
    Parameters:
    None (None): This module does not accept parameters.
    
    Returns:
    None: This module does not return a value.
"""

import os

import constant
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError(f"{constant.MSG_MISSING_ENV}: DATABASE_URL")

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
