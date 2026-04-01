"""Database operations for user endpoints."""

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
from schemas import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(request: User, db: Session):
    """Create and return a user with hashed password."""
    existing_user = db.query(models.User).filter(models.User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    hashed_password = pwd_context.hash(request.password)

    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session):
    """Fetch and return all users."""
    return db.query(models.User).all()


def get_user_by_id(id: int, db: Session):
    """Fetch and return one user by id."""
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def delete_user(id: int, db: Session):
    """Delete one user by id and return a confirmation message."""
    user = db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.commit()
    return f"User with id {id} deleted successfully"

