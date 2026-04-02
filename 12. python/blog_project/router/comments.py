from repository import comments as comments_repository
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from database import get_db
import schemas
import oauth2

router = APIRouter(tags=["comments"])

@router.post("/comment/{blog_id}", status_code=status.HTTP_201_CREATED)
def create_comment(
    blog_id: int,
    request: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user),
):
    """Create a new comment for a blog post."""
    return comments_repository.create_comment(blog_id, request, db, current_user)

@router.get("/show_comment", response_model=list[schemas.Comment], status_code=status.HTTP_200_OK)
def show_comment(    
    page_no: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    get_current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    """Return a paginated list of all comments."""
    return comments_repository.get_all_comments(page_no, limit,db)

@router.get('/show_comment/{blog_id}', response_model=list[schemas.Comment], status_code=status.HTTP_200_OK)
def show_blog_comment(    
    blog_id: int,
    page_no: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    get_current_user: schemas.TokenData = Depends(oauth2.get_current_user)):

    """Return paginated comments for one blog post."""
    return comments_repository.get_all_comments_by_blog(blog_id, page_no, limit, db)
