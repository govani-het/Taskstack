from repository import reply as reply_repository
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
import schemas

router = APIRouter(tags=["reply"])

@router.post("/reply/{id}", status_code=status.HTTP_201_CREATED)
def create_reply(request: schemas.ReplyCreate, db: Session = Depends(get_db)):
    """Create a reply for a comment."""
    return reply_repository.create_reply(request, db)
