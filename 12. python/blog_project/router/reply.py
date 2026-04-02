from repository import reply as reply_repository
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
import schemas
import oauth2

router = APIRouter(tags=["reply"])

@router.post("/reply/{comment_id}", status_code=status.HTTP_201_CREATED)
def create_reply(
    comment_id: int,
    request: schemas.ReplyCreate,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user),
):
    """
        Handles the create reply operation.
        
        Parameters:
        comment id (int): The comment id value used by this function.
        request (schemas ReplyCreate): The request value used by this function.
        db (Session): The db value used by this function.
        current user (schemas TokenData): The current user value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    return reply_repository.create_reply(comment_id, request, db, current_user)
