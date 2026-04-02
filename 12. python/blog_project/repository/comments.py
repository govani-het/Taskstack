from sqlalchemy.orm import Session
from fastapi import HTTPException

import models
from schemas import CommentCreate, TokenData


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
         raise HTTPException(status_code=404, detail="Comments not found")
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
        raise HTTPException(status_code=404, detail="Comments not found")
    
    return comments_by_blog