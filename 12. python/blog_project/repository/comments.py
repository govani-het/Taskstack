from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

import models
from schemas import CommentCreate, TokenData
import constant

def create_comment(id: int, request: CommentCreate, db: Session, current_user: TokenData):
    """
        Handles the create comment operation.
        
        Parameters:
        id (int): The id value used by this function.
        request (CommentCreate): The request value used by this function.
        db (Session): The db value used by this function.
        current user (TokenData): The current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    if current_user.user_id is None:
        raise HTTPException(status_code=401, detail=constant.MSG_INVALID_CREDENTIALS)

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=constant.MSG_BLOG_NOT_FOUND)

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
    """
        Handles the get all comments operation.
        
        Parameters:
        page no (Any): The page no value used by this function.
        limit (Any): The limit value used by this function.
        db (Session): The db value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    skip = (int(page_no) - 1) * int(limit)

    comments = db.query(models.Comment).offset(skip).limit(limit).all()

    if not comments:
         raise HTTPException(status_code=404, detail=constant.MSG_COMMENT_NOT_FOUND)
    return comments

def get_all_comments_by_blog(blog_id, page_no, limit, db:Session):
    """
        Handles the get all comments by blog operation.
        
        Parameters:
        blog id (Any): The blog id value used by this function.
        page no (Any): The page no value used by this function.
        limit (Any): The limit value used by this function.
        db (Session): The db value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    skip = (int(page_no) - 1) * int(limit)

    comments_by_blog =  db.query(models.Comment).filter(models.Comment.blog_id == blog_id).offset(skip).limit(limit).all()

    if not comments_by_blog:
        raise HTTPException(status_code=404, detail=constant.MSG_COMMENT_NOT_FOUND)
    
    return comments_by_blog


def delete_comment(comment_id: int, db: Session, current_user: TokenData):
    """
        Handles the delete comment operation.
        
        Parameters:
        comment id (int): The comment id value used by this function.
        db (Session): The db value used by this function.
        current user (TokenData): The current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    if current_user.user_id is None:
        raise HTTPException(status_code=401, detail=constant.MSG_INVALID_CREDENTIALS)

    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail=constant.MSG_COMMENT_NOT_FOUND)

    if comment.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail=constant.MSG_DELETE_ONLY_OWN_COMMENT)

    try:
        db.query(models.Reply).filter(models.Reply.comment_id == comment_id).delete(
            synchronize_session=False
        )
        db.delete(comment)
        db.commit()
        return {constant.RESP_KEY_MESSAGE: constant.MSG_COMMENT_DELETED}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail=constant.MSG_FAILED_DELETE_COMMENT)
