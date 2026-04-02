from sqlalchemy.orm import Session
from fastapi import HTTPException

import models
from schemas import CommentCreate, TokenData


def create_comment(id: int, request: CommentCreate, db: Session, current_user: TokenData):
    """Create and persist a comment for a specific blog."""
    if current_user.user_id is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    new_comment = models.Comment(
        content=request.content,
        blog_id=id,
        user_id=current_user.user_id,
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_all_comments(page_no, limit,db: Session):
    """Fetch comments using basic page and limit pagination."""
    skip = (int(page_no) - 1) * int(limit)
    return db.query(models.Comment).offset(skip).limit(limit).all()

def get_all_comments_by_blog(blog_id, page_no, limit, db:Session):
    """Fetch paginated comments that belong to a specific blog."""
    skip = (int(page_no) - 1) * int(limit)

    return db.query(models.Comment).filter(models.Comment.blog_id == blog_id).offset(skip).limit(limit).all()
