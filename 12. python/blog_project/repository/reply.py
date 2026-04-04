
from fastapi import HTTPException
from schemas import ReplyCreate, TokenData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import models
import constant


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
        raise HTTPException(status_code=401, detail=constant.MSG_INVALID_CREDENTIALS)

    comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    if not comment:
        raise HTTPException(status_code=404, detail=constant.MSG_COMMENT_NOT_FOUND)

    new_reply =models.Reply(
        content=request.content,
        comment_id=id,
        user_id=current_user.user_id,
    )

    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)
    return new_reply


def delete_reply(reply_id: int, db: Session, current_user: TokenData):
    """
        Handles the delete reply operation.
        
        Parameters:
        reply id (int): The reply id value used by this function.
        db (Session): The db value used by this function.
        current user (TokenData): The current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    if current_user.user_id is None:
        raise HTTPException(status_code=401, detail=constant.MSG_INVALID_CREDENTIALS)

    reply = db.query(models.Reply).filter(models.Reply.id == reply_id).first()
    if not reply:
        raise HTTPException(status_code=404, detail=constant.MSG_REPLY_NOT_FOUND)

    if reply.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail=constant.MSG_DELETE_ONLY_OWN_REPLY)

    try:
        db.delete(reply)
        db.commit()
        return {constant.RESP_KEY_MESSAGE: constant.MSG_REPLY_DELETED}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail=constant.MSG_FAILED_DELETE_REPLY)
