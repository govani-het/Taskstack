
from fastapi import HTTPException
from schemas import ReplyCreate, TokenData
from sqlalchemy.orm import Session
import models


def create_reply(id: int, request: ReplyCreate, db: Session, current_user: TokenData):
    """Create and persist a reply for a specific comment."""
    if current_user.user_id is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    new_reply =models.Reply(
        content=request.content,
        comment_id=id,
        user_id=current_user.user_id,
    )

    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)
    return new_reply
