
from schemas import ReplyCreate
from sqlalchemy.orm import Session
import models


def create_reply(id, request: ReplyCreate, db: Session):
    new_reply =models.Reply(
        content=request.content,
        comment_id=id,
        user_id=request.user_id,
    )

    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)
    return new_reply

