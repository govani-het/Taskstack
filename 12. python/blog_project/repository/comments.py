from sqlalchemy.orm import Session

import models
from schemas import CommentCreate


def create_comment(id,request: CommentCreate, db: Session):
    """Create and persist a comment for a specific blog."""
    new_comment = models.Comment(
        content=request.content,
        blog_id=id,
        user_id=request.user_id,
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

