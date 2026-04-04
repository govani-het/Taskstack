

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import BlogCreate, BlogUpdate, ShowBlog, TokenData
from repository import blog as blog_repository
import oauth2
import constant

router = APIRouter(tags=["blogs"])


@router.post("/blog/upload", response_model=ShowBlog, status_code=status.HTTP_201_CREATED)
def create_with_upload(
    title: str = Form(...),
    body: str = Form(...),
    images: list[UploadFile] | None = File(default=None),
    db: Session = Depends(get_db),
    get_current_user: TokenData = Depends(oauth2.get_current_user),
):
    """
        Handles create blog with uploaded images.

        Parameters:
        title (str): Blog title.
        body (str): Blog body.
        images (list[UploadFile] | None): Uploaded blog images.
        db (Session): Database session.
        get current user (TokenData): Authenticated user information.

        Returns:
        Any: The result produced by this function.
    """
    return blog_repository.create_blog_with_uploaded_images(
        title=title,
        body=body,
        images=images or [],
        db=db,
        user_id=get_current_user.user_id,
    )

@router.get("/show_blog", response_model=list[ShowBlog], status_code=status.HTTP_200_OK)
def all(
    db: Session = Depends(get_db),
    get_current_user: TokenData = Depends(oauth2.get_current_user),
):
    """
        Handles the all operation.
        
        Parameters:
        db (Session): The db value used by this function.
        get current user (TokenData): The get current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """

    return blog_repository.get_all_blogs(db)

@router.get("/search_blog", response_model=list[ShowBlog], status_code=status.HTTP_200_OK)
def search_blog(
    search: str,
    db: Session = Depends(get_db),
    get_current_user: TokenData = Depends(oauth2.get_current_user),
):
    """
        Handles the search blog operation.
        
        Parameters:
        search (str): The search value used by this function.
        db (Session): The db value used by this function.
        get current user (TokenData): The get current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    return blog_repository.search_blogs(db, search)

@router.get("/blog/{id}", response_model=ShowBlog, status_code=status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db), get_current_user: TokenData = Depends(oauth2.get_current_user)):
    """
        Handles the show operation.
        
        Parameters:
        id (int): The id value used by this function.
        db (Session): The db value used by this function.
        get current user (TokenData): The get current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """

    return blog_repository.get_blog(id, db)

@router.delete("/blog/{id}", status_code=status.HTTP_200_OK)
def destroy(
    id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(oauth2.get_current_user),
):
    """
        Handles the destroy operation.
        
        Parameters:
        id (int): The id value used by this function.
        db (Session): The db value used by this function.
        current user (TokenData): The current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """

    return blog_repository.delete_blog(id, db, current_user)

@router.patch("/blog/{id}", status_code=status.HTTP_200_OK)
def update_partial(
    id: int,
    request: BlogUpdate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(oauth2.get_current_user)
):
    """
        Handles the update partial operation.
        
        Parameters:
        id (int): The id value used by this function.
        request (BlogUpdate): The request value used by this function.
        db (Session): The db value used by this function.
        current user (TokenData): The current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """

    return blog_repository.update_blog_partial(id, request, db, current_user)

@router.post("/like_blog/{id}", status_code=status.HTTP_200_OK)
def like_blog(
    id:int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(oauth2.get_current_user)
):
    """
        Handles the like blog operation.
        
        Parameters:
        id (int): The id value used by this function.
        db (Session): The db value used by this function.
        current user (TokenData): The current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    return blog_repository.like_blog(blog_id=id,db=db,user_id=current_user.user_id)

@router.get("/sort_blog", response_model=list[ShowBlog],status_code=status.HTTP_200_OK)
def sort_blog(db:Session = Depends(get_db), get_current_user: TokenData = Depends(oauth2.get_current_user)):
    """
        Handles the sort blog operation.
        
        Parameters:
        db (Session): The db value used by this function.
        get current user (TokenData): The get current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    return blog_repository.sort_blog(db)
