"""Database operations for blog endpoints."""

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

import models
from schemas import BlogCreate, BlogUpdate, TokenData


def create_blog(request: BlogCreate, db: Session, user_id:int):
    """Create and return a new blog entry."""
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
    """Fetch and return all blog entries."""
    blogs = db.query(models.Blog).all()

    for blog in blogs:
        if blog.comments:
            blog.comments = sorted(
                blog.comments,
                key=lambda c: c.created_at,
                reverse=True
            )[:3]

    return blogs 


def search_blogs(db: Session, search: str):
    """Fetch and return blogs matching search text in title or body."""
    search_value = search.strip()
    if not search_value:
        raise HTTPException(status_code=400, detail="Search text is required")

    blogs = db.query(models.Blog).filter(
        or_(
            models.Blog.title.ilike(f"%{search_value}%"),
            models.Blog.body.ilike(f"%{search_value}%"),
        )
    ).all()

    for blog in blogs:
        if blog.comments:
            blog.comments = sorted(
                blog.comments,
                key=lambda c: c.created_at,
                reverse=True
            )[:3]

    return blogs


def get_blog(id: int, db: Session):
    """Fetch and return one blog by id."""
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    return blog


def delete_blog(id: int, db: Session, current_user: TokenData):
    """Delete one blog by id and return a confirmation message."""
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

    """Update only provided fields for a blog and return the refreshed record."""
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
        
    blog = db.query(models.Blog).order_by(models.Blog.created_at.desc()).all()

    if not blog:
        return {"Error": "Blog Not Found"}
    
    return blog
