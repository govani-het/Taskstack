from repository import comments as comments_repository
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
import schemas

router = APIRouter(tags=["comments"])

@router.post("/comment/{id}", status_code=status.HTTP_201_CREATED)
def create_comment(blog_id,request: schemas.CommentCreate, db: Session = Depends(get_db)):
    return comments_repository.create_comment(blog_id,request, db)


@router.get("/show_comment/{page_no}/{limit}", response_model=list[schemas.Comment], status_code=status.HTTP_200_OK)
def show_comment(page_no, limit,db: Session = Depends(get_db)):
    return comments_repository.get_all_comments(page_no, limit,db)

@router.get('/show_comment/{blog_id}/{page_no}/{limit}', response_model=list[schemas.Comment], status_code=status.HTTP_200_OK)
def show_blog_comment(blog_id, page_no, limit, db: Session = Depends(get_db)):
    return comments_repository.get_all_comments_by_blog(blog_id, page_no, limit,db)