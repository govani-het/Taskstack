"""
    Defines the user module.
    
    Parameters:
    None (None): This module does not accept parameters.
    
    Returns:
    None: This module does not return a value.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, ShowUser
from repository import user as user_repository
import oauth2,schemas

router = APIRouter(tags=["users"])

@router.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    """
        Handles the create user operation.
        
        Parameters:
        request (UserCreate): The request value used by this function.
        db (Session): The db value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    return user_repository.create_user(request, db)

@router.get("/show_user", response_model=list[ShowUser], status_code=status.HTTP_200_OK)
def show_user(db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    """
        Handles the show user operation.
        
        Parameters:
        db (Session): The db value used by this function.
        current user (schemas TokenData): The current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    return user_repository.get_all_users(db)

@router.get("/show_user/{id}", status_code=status.HTTP_200_OK)
def show_user_by_id(id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    """
        Handles the show user by id operation.
        
        Parameters:
        id (int): The id value used by this function.
        db (Session): The db value used by this function.
        current user (schemas TokenData): The current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    return user_repository.get_user_by_id(id, db)


@router.delete("/delete_user", status_code=status.HTTP_200_OK)
def delete_user(db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    """
        Handles the delete user operation.
        
        Parameters:
        id (int): The id value used by this function.
        db (Session): The db value used by this function.
        current user (schemas TokenData): The current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    return user_repository.delete_user(current_user.user_id, db)

@router.post('/my_fav/{id}', status_code=status.HTTP_200_OK)
def my_fav_blog(id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    """
        Handles the my fav blog operation.
        
        Parameters:
        id (int): The id value used by this function.
        db (Session): The db value used by this function.
        current user (schemas TokenData): The current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    return user_repository.my_fav_blog(blog_id=id,db=db,user_id=current_user.user_id)
