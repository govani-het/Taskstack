
from fastapi import HTTPException
from schemas import ReplyCreate, TokenData
from sqlalchemy.orm import Session
import models


def create_reply(id: int, request: ReplyCreate, db: Session, current_user: TokenData):
    """
        Handles the create reply operation.
        
        Parameters:
        id (int): The id value used by this function.
        request (ReplyCreate): The request value used by this function.
        db (Session): The db value used by this function.
        current user (TokenData): The current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
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
