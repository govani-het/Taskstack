"""
    Defines the blog module.
    
    Parameters:
    None (None): This module does not accept parameters.
    
    Returns:
    None: This module does not return a value.
"""

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

import models
from schemas import BlogCreate, BlogUpdate, TokenData



def create_blog(request: BlogCreate, db: Session, user_id:int):
    """
        Handles the create blog operation.
        
        Parameters:
        request (BlogCreate): The request value used by this function.
        db (Session): The db value used by this function.
        user id (int): The user id value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        user_id=user_id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def get_all_blogs(db: Session):
    """
        Handles the get all blogs operation.
        
        Parameters:
        db (Session): The db value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    blogs = db.query(models.Blog).all()

    if not blogs:
        raise HTTPException(status_code=404, detail="Blog not found")

    for blog in blogs:
        if blog.comments:
            blog.comments = sorted(
                blog.comments,
                key=lambda c: c.created_at,
                reverse=True
            )[:3]

    return blogs 

def search_blogs(db: Session, search: str):
    """
        Handles the search blogs operation.
        
        Parameters:
        db (Session): The db value used by this function.
        search (str): The search value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    search_value = search.strip()
    if not search_value:
        raise HTTPException(status_code=400, detail="Search text is required")

    blogs = db.query(models.Blog).filter(
        or_(
            models.Blog.title.ilike(f"%{search_value}%"),
            models.Blog.body.ilike(f"%{search_value}%"),
        )
    ).all()

    if not blogs:
        raise HTTPException(status_code=404, detail="Blog not found")

    for blog in blogs:
        if blog.comments:
            blog.comments = sorted(
                blog.comments,
                key=lambda c: c.created_at,
                reverse=True
            )[:3]

    return blogs

def get_blog(id: int, db: Session):
    """
        Handles the get blog operation.
        
        Parameters:
        id (int): The id value used by this function.
        db (Session): The db value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    return blog

def delete_blog(id: int, db: Session, current_user: TokenData):
    """
        Handles the delete blog operation.
        
        Parameters:
        id (int): The id value used by this function.
        db (Session): The db value used by this function.
        current user (TokenData): The current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    if current_user.user_id is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if blog.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can delete only your own blog")

    db.delete(blog)
    db.commit()
    return f"Blog with id {id} deleted successfully"

def update_blog_partial(id: int, request: BlogUpdate, db: Session, current_user: TokenData):

    """
        Handles the update blog partial operation.
        
        Parameters:
        id (int): The id value used by this function.
        request (BlogUpdate): The request value used by this function.
        db (Session): The db value used by this function.
        current user (TokenData): The current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    if current_user.user_id is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if blog.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can update only your own blog")

    data = request.model_dump(exclude_unset=True)   

    if not data:
        raise HTTPException(status_code=400, detail="No data provided")

    for key, value in data.items():
        setattr(blog, key, value)

    db.commit()
    db.refresh(blog)
    return blog

def like_blog(blog_id: int, db: Session, user_id:int):
    """
        Handles the like blog operation.
        
        Parameters:
        blog id (int): The blog id value used by this function.
        db (Session): The db value used by this function.
        user id (int): The user id value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    like = db.query(models.Like).filter(models.Like.user_id == user_id, models.Like.blog_id == blog_id).first()

    if like:
        db.delete(like)
        db.commit()
        return {"message": "Blog disliked successfully"}
    else:
        new_like = models.Like(
            blog_id=blog_id,
            user_id=user_id
        )
        db.add(new_like)
        db.commit()

        return {"message": "Blog liked successfully"}
    
def sort_blog(db):
    """
        Handles the sort blog operation.
        
        Parameters:
        db (Any): The db value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    blog = db.query(models.Blog).order_by(models.Blog.created_at.desc()).all()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    return blog
