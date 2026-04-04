
from pathlib import Path
from typing import List, Tuple
from uuid import uuid4
import constant
from fastapi import HTTPException, UploadFile
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

import models
from schemas import (
    BlogCreate,
    BlogUpdate,
    MAX_BLOG_IMAGES,
    TokenData,
)


UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads" / "blogs"
UPLOAD_CHUNK_SIZE = 1024 * 1024
MAX_UPLOAD_IMAGE_SIZE = 5 * 1024 * 1024
ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/gif",
}
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}



def validate_blog_payload(title: str, body: str) -> Tuple[str, str]:
    """
        Handles the validate blog payload operation.
        
        Parameters:
        title (str): The title value used by this function.
        body (str): The body value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    title = title.strip()
    body = body.strip()

    if not title:
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    if not body:
        raise HTTPException(status_code=400, detail="Body cannot be empty")

    return title, body


def validate_uploaded_images(images: List[UploadFile]) -> None:
    """
        Handles the validate uploaded images operation.
        
        Parameters:
        images (List[UploadFile]): The images value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    if len(images) > MAX_BLOG_IMAGES:
        raise HTTPException(
            status_code=400,
            detail=f"A blog can have at most {MAX_BLOG_IMAGES} images",
        )

    for image in images:
        if image.content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported image type: {image.content_type}",
            )


def resolve_extension(image: UploadFile) -> str:
    """
        Handles the resolve extension operation.
        
        Parameters:
        image (UploadFile): The image value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    extension = Path(image.filename or "").suffix.lower()
    if extension in ALLOWED_IMAGE_EXTENSIONS:
        return extension

    content_type_to_extension = {
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "image/gif": ".gif",
    }
    return content_type_to_extension.get(image.content_type, ".jpg")


def save_uploaded_image(image: UploadFile) -> Tuple[str, Path]:
    """
        Handles the save uploaded image operation.
        
        Parameters:
        image (UploadFile): The image value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    file_name = f"{uuid4().hex}{resolve_extension(image)}"
    file_path = UPLOAD_DIR / file_name

    total_size = 0
    try:
        with file_path.open("wb") as buffer:
            while True:
                chunk = image.file.read(UPLOAD_CHUNK_SIZE)
                if not chunk:
                    break

                total_size += len(chunk)
                if total_size > MAX_UPLOAD_IMAGE_SIZE:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Image '{image.filename}' exceeds 5 MB limit",
                    )
                buffer.write(chunk)

        if total_size == 0:
            raise HTTPException(
                status_code=400,
                detail=f"Image '{image.filename}' is empty",
            )
    except HTTPException:
        if file_path.exists():
            file_path.unlink()
        raise
    except OSError:
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail="Failed to save uploaded image")

    return f"/uploads/blogs/{file_name}", file_path


def create_blog_with_uploaded_images(
    title: str,
    body: str,
    images: List[UploadFile],
    db: Session,
    user_id: int,
):
    """
        Handles the create blog with uploaded images operation.
        
        Parameters:
        title (str): The title value used by this function.
        body (str): The body value used by this function.
        images (List[UploadFile]): The images value used by this function.
        db (Session): The db value used by this function.
        user id (int): The user id value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    if user_id is None:
        raise HTTPException(status_code=401, detail=constant.MSG_INVALID_CREDENTIALS)

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=constant.MSG_USER_NOT_FOUND)

    title, body = validate_blog_payload(title, body)
    validate_uploaded_images(images)

    saved_files: List[Path] = []
   
    new_blog = models.Blog(
        title=title,
        body=body,
        user_id=user_id,
    )
    db.add(new_blog)
    db.flush()

    for image in images:
        image_url, file_path = save_uploaded_image(image)
        saved_files.append(file_path)
        db.add(models.BlogImage(blog_id=new_blog.id, image_url=image_url))

    db.commit()
    db.refresh(new_blog)
    return new_blog


def get_all_blogs(db: Session):
    """
        Handles the get all blogs operation.
        
        Parameters:
        db (Session): The db value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    blogs = (
        db.query(models.Blog)
        .options(
            selectinload(models.Blog.comments).selectinload(models.Comment.replies),
            selectinload(models.Blog.images),
            selectinload(models.Blog.creator),
        )
        .all()
    )

    if not blogs:
        raise HTTPException(status_code=404, detail=constant.MSG_BLOG_NOT_FOUND)

    for blog in blogs:
        if blog.comments:
            blog.comments = sorted(
                blog.comments,
                key=lambda c: c.created_at,
                reverse=True
            )[:3]

    return blogs 

def search_blogs(db: Session, search: str):
    """
        Handles the search blogs operation.
        
        Parameters:
        db (Session): The db value used by this function.
        search (str): The search value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    search_value = search.strip()
    if not search_value:
        raise HTTPException(status_code=400, detail="Search text is required")

    blogs = (
        db.query(models.Blog)
        .options(
            selectinload(models.Blog.comments).selectinload(models.Comment.replies),
            selectinload(models.Blog.images),
            selectinload(models.Blog.creator),
        )
        .filter(
            or_(
                models.Blog.title.ilike(f"%{search_value}%"),
                models.Blog.body.ilike(f"%{search_value}%"),
            )
        )
        .all()
    )

    if not blogs:
        raise HTTPException(status_code=404, detail=constant.MSG_BLOG_NOT_FOUND)

    for blog in blogs:
        if blog.comments:
            blog.comments = sorted(
                blog.comments,
                key=lambda c: c.created_at,
                reverse=True
            )[:3]

    return blogs

def get_blog(id: int, db: Session):
    """
        Handles the get blog operation.
        
        Parameters:
        id (int): The id value used by this function.
        db (Session): The db value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    blog = (
        db.query(models.Blog)
        .options(
            selectinload(models.Blog.comments).selectinload(models.Comment.replies),
            selectinload(models.Blog.images),
            selectinload(models.Blog.creator),
        )
        .filter(models.Blog.id == id)
        .first()
    )
    if not blog:
        raise HTTPException(status_code=404, detail=constant.MSG_BLOG_NOT_FOUND)

    return blog

def delete_blog(id: int, db: Session, current_user: TokenData):
    """
        Handles the delete blog operation.
        
        Parameters:
        id (int): The id value used by this function.
        db (Session): The db value used by this function.
        current user (TokenData): The current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=constant.MSG_BLOG_NOT_FOUND)

    if current_user.user_id is None:
        raise HTTPException(status_code=401, detail=constant.MSG_INVALID_CREDENTIALS)

    if blog.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can delete only your own blog")

    db.delete(blog)
    db.commit()
    return f"Blog with id {id} deleted successfully"

def update_blog_partial(id: int, request: BlogUpdate, db: Session, current_user: TokenData):

    """
        Handles the update blog partial operation.
        
        Parameters:
        id (int): The id value used by this function.
        request (BlogUpdate): The request value used by this function.
        db (Session): The db value used by this function.
        current user (TokenData): The current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404, detail=constant.MSG_BLOG_NOT_FOUND)

    if current_user.user_id is None:
        raise HTTPException(status_code=401, detail=constant.MSG_INVALID_CREDENTIALS)

    if blog.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can update only your own blog")

    data = request.model_dump(exclude_unset=True)   

    if not data:
        raise HTTPException(status_code=400, detail="No data provided")

    for key, value in data.items():
        setattr(blog, key, value)

    db.commit()
    db.refresh(blog)
    return blog

def like_blog(blog_id: int, db: Session, user_id:int):
    """
        Handles the like blog operation.
        
        Parameters:
        blog id (int): The blog id value used by this function.
        db (Session): The db value used by this function.
        user id (int): The user id value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    like = db.query(models.Like).filter(models.Like.user_id == user_id, models.Like.blog_id == blog_id).first()

    if like:
        db.delete(like)
        db.commit()
        return {"message": "Blog disliked successfully"}
    else:
        new_like = models.Like(
            blog_id=blog_id,
            user_id=user_id
        )
        db.add(new_like)
        db.commit()

        return {"message": "Blog liked successfully"}
    
def sort_blog(db):
    """
        Handles the sort blog operation.
        
        Parameters:
        db (Any): The db value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    blog = (
        db.query(models.Blog)
        .options(
            selectinload(models.Blog.comments).selectinload(models.Comment.replies),
            selectinload(models.Blog.images),
            selectinload(models.Blog.creator),
        )
        .order_by(models.Blog.created_at.desc())
        .all()
    )

    if not blog:
        raise HTTPException(status_code=404, detail=constant.MSG_BLOG_NOT_FOUND)
    
    return blog
