from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload

import models
import schemas


def create_profile(request: schemas.UserProfile, db: Session, user_id: int):
    """
        Handles the create profile operation.
        
        Parameters:
        request (schemas UserProfile): The request value used by this function.
        db (Session): The db value used by this function.
        user id (int): The user id value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
    if user:
        raise HTTPException(status_code=404, detail="you have already created Profile")

    new_profile = models.UserProfile(
        first_name=request.first_name,
        last_name=request.last_name,
        dob=request.dob,
        user_id=user_id,
    )

    db.add(new_profile)
    db.commit()
    return {"message": "Profile Created Successfully"}

def update_profile(request: schemas.UserProfileUpdate, db: Session, user_id: int):
    """
        Handles the update profile operation.
        
        Parameters:
        request (schemas UserProfileUpdate): The request value used by this function.
        db (Session): The db value used by this function.
        user id (int): The user id value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    data = request.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(status_code=400, detail="No data provided")

    for key, value in data.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return {"message": "Profile Updated Successfully", "profile": profile}

def delete_profile(db: Session, user_id: int):
    """
        Handles the delete profile operation.
        
        Parameters:
        db (Session): The db value used by this function.
        user id (int): The user id value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    user_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id==user_id).first()
    db.delete(user_profile)
    db.commit()
    return {"message": "Profile Deleted Successfully"}

def show_profile(db: Session, user_id: int):
    """
        Handles the show profile operation.
        
        Parameters:
        db (Session): The db value used by this function.
        user id (int): The user id value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """

    user_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id==user_id).first()

    if not user_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return user_profile

def show_my_blog(page_no,limit,db: Session, user_id: int):
    """
        Handles the show my blog operation.
        
        Parameters:
        page no (Any): The page no value used by this function.
        limit (Any): The limit value used by this function.
        db (Session): The db value used by this function.
        user id (int): The user id value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    skip = (int(page_no) - 1) * int(limit)

    blogs = (
        db.query(
            models.Blog,
            func.count(models.Like.id).label("total_like_count")
        )
        .outerjoin(models.Like, models.Like.blog_id == models.Blog.id)
        .options(
            selectinload(models.Blog.comments).selectinload(models.Comment.replies)
        )
        .filter(models.Blog.user_id == user_id)
        .group_by(models.Blog.id)
        .order_by(models.Blog.created_at.desc()).offset(skip).limit(limit)
        .all()
    )

    if not blogs:
        raise HTTPException(status_code=404, detail="Blog not found")

    result = []
    for blog, total_like_count in blogs:
        recent_comments = sorted(
            blog.comments,
            key=lambda comment: comment.created_at,
            reverse=True
        )[:3]

        comments_data = []
        for comment in recent_comments:
            sorted_replies = sorted(
                comment.replies,
                key=lambda reply: reply.created_at,
                reverse=True
            )

            comments_data.append(
                {
                    "id": comment.id,
                    "content": comment.content,
                    "created_at": comment.created_at,
                    "replies": [
                        {
                            "id": reply.id,
                            "content": reply.content,
                            "created_at": reply.created_at,
                        }
                        for reply in sorted_replies
                    ],
                }
            )

        result.append(
            {
                "title": blog.title,
                "body": blog.body,
                "created_at": blog.created_at,
                "total_like_count": total_like_count,
                "comments": comments_data,
            }
        )

    return result

def show_my_fav_blog(page_no,limit,db:Session, user_id: int):
    """
        Handles the show my fav blog operation.
        
        Parameters:
        page no (Any): The page no value used by this function.
        limit (Any): The limit value used by this function.
        db (Session): The db value used by this function.
        user id (int): The user id value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    skip = (int(page_no) - 1) * int(limit)

    fav_blog = db.query(models.MyFav).filter(models.MyFav.user_id==user_id).offset(skip).limit(limit).all()

    if not fav_blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    return fav_blog
