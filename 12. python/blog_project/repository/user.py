

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
from schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(request: UserCreate, db: Session):
    """
        Handles the create user operation.
        
        Parameters:
        request (UserCreate): The request value used by this function.
        db (Session): The db value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    existing_user = db.query(models.User).filter(models.User.email == request.email, models.User.name == request.name).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="User already registered")

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
    """
        Handles the get all users operation.
        
        Parameters:
        db (Session): The db value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """

    users = db.query(models.User).all()

    if not users:
        raise HTTPException(status_code=404, detail="User Not Found")

    return users


def get_user_by_id(id: int, db: Session):
    """
        Handles the get user by id operation.
        
        Parameters:
        id (int): The id value used by this function.
        db (Session): The db value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def delete_user(id: int, db: Session):
    """
        Handles the delete user operation.
        
        Parameters:
        id (int): The id value used by this function.
        db (Session): The db value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    user = db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.commit()
    return f"User with id {id} deleted successfully"


def my_fav_blog(blog_id:int, db:Session, user_id:int):
    """
        Handles the my fav blog operation.
        
        Parameters:
        blog id (int): The blog id value used by this function.
        db (Session): The db value used by this function.
        user id (int): The user id value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    my_fav = db.query(models.MyFav).filter(models.MyFav.user_id==user_id, models.MyFav.blog_id==blog_id).first()
    try:
        if my_fav:
            db.delete(my_fav)
            db.commit()
            return {"message": "Blog removed from saved items"}
        else:
            new_fav= models.MyFav(
                user_id=user_id,
                blog_id=blog_id
            )
            db.add(new_fav)
            db.commit()
            return {"message": "Blog saved successfully"}
    except Exception:
        raise HTTPException (status_code=404, detail="Blog Not Found")
