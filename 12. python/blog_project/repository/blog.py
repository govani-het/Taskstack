"""Database operations for blog endpoints."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
from schemas import BlogCreate, BlogUpdate


def create_blog(request: BlogCreate, db: Session):
    """Create and return a new blog entry."""
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        user_id=request.user_id,
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


def get_blog(id: int, db: Session):
    """Fetch and return one blog by id."""
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    return blog


def delete_blog(id: int, db: Session):
    """Delete one blog by id and return a confirmation message."""
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    db.commit()
    return f"Blog with id {id} deleted successfully"


def update_blog_partial(id: int, request: BlogUpdate, db: Session):
    """Update only provided fields for a blog and return the refreshed record."""
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    data = request.model_dump(exclude_unset=True)   # ✅ FIX

    if not data:
        raise HTTPException(status_code=400, detail="No data provided")

    if "user_id" in data:
        user = db.query(models.User).filter(models.User.id == data["user_id"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

    for key, value in data.items():
        setattr(blog, key, value)

    db.commit()
    db.refresh(blog)
