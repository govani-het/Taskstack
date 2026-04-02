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
    """Create a reply for a comment."""
    return reply_repository.create_reply(comment_id, request, db, current_user)
