from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from database import get_db
import schemas
from repository import user_profile as user_profile_repository
import oauth2

router = APIRouter(tags=["users_profile"])

@router.post('/create_user_profile', status_code=status.HTTP_201_CREATED)
def create_user_profile(
        request: schemas.UserProfile, 
        db: Session = Depends(get_db), 
        current_user: schemas.TokenData = Depends(oauth2.get_current_user)
        ):
    return user_profile_repository.create_profile(request,db,current_user.user_id)

@router.patch('/update_user_profile', status_code=status.HTTP_200_OK)
def update_user_profile(
        request: schemas.UserProfileUpdate,
        db: Session = Depends(get_db), 
        current_user: schemas.TokenData = Depends(oauth2.get_current_user)
    ):
    return user_profile_repository.update_profile(request, db, current_user.user_id)

@router.delete('/delete_user_profile', status_code=status.HTTP_200_OK)
def update_user_profile(
        db: Session = Depends(get_db), 
        current_user: schemas.TokenData = Depends(oauth2.get_current_user)
    ):
    return user_profile_repository.delete_profile(db, current_user.user_id)

@router.get('/show_user_profile', response_model=schemas.UserProfile, status_code=status.HTTP_200_OK)
def show_user_profile(
        db: Session = Depends(get_db), 
        current_user: schemas.TokenData = Depends(oauth2.get_current_user)
    ):
    return user_profile_repository.show_profile(db, current_user.user_id)

@router.get("/show_my_blog", status_code=status.HTTP_200_OK)
def show_my_blog(
    page_no: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db), 
    current_user: schemas.TokenData = Depends(oauth2.get_current_user)
):
    return user_profile_repository.show_my_blog(page_no,limit,db,current_user.user_id)

@router.get("/show_my_fav_blog", response_model=list[schemas.ShowMyFavBlog], status_code=status.HTTP_200_OK)
def show_my_fav_blog(
    page_no: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db), 
    current_user: schemas.TokenData = Depends(oauth2.get_current_user)
    ):
    return user_profile_repository.show_my_fav_blog(page_no,limit,db,current_user.user_id)