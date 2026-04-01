"""User router with account creation and basic read/delete endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import User, ShowUser
from repository import user as user_repository


router = APIRouter(tags=["users"])

@router.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(request: User, db: Session = Depends(get_db)):
    """Create a user and store a hashed password."""
    return user_repository.create_user(request, db)

@router.get("/show_user", response_model=list[ShowUser], status_code=status.HTTP_200_OK)
def show_user(db: Session = Depends(get_db)):
    """Return all users."""
    return user_repository.get_all_users(db)

@router.get("/show_user/{id}", status_code=status.HTTP_200_OK)
def show_user_by_id(id: int, db: Session = Depends(get_db)):
    """Return one user by identifier."""
    return user_repository.get_user_by_id(id, db)


@router.delete("/delete_user/{id}", status_code=status.HTTP_200_OK)
def delete_user(id: int, db: Session = Depends(get_db)):
    """Delete a user by identifier."""
    return user_repository.delete_user(id, db)
