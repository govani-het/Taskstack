from sqlalchemy.orm import Session

import models
from schemas import CommentCreate


def create_comment(id,request: CommentCreate, db: Session):
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
    skip = (int(page_no) - 1) * int(limit)
    return db.query(models.Comment).offset(skip).limit(limit).all()


