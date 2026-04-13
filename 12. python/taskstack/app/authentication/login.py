from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
import bcrypt

from app.schemas import login_schemas
from app.config.database import get_db
from app.repositories.auth_query import get_active_user_by_email
from app.authentication.role_base_auth_token import create_access_token, create_refresh_token
from datetime import timedelta
import os

router = APIRouter(
    prefix="/app/v1/auth",
    tags=["login"],
)


def verify_password(plain_password: str, stored_password: str) -> bool:
    if not stored_password:
        return False

    if stored_password.startswith(("$2a$", "$2b$", "$2y$")):
        try:
            return bcrypt.checkpw(plain_password.encode("utf-8"), stored_password.encode("utf-8"))
        except ValueError:
            return False

    return plain_password == stored_password


@router.post("/login", response_model=login_schemas.Token)
async def login(request: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_active_user_by_email(db, request.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_data = {
        "sub": user.email,
        "id": str(user.id),
        "role": user.role.name if user.role else None,
        "organization_id": str(user.organization_id) if user.organization_id else None,
    }

    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
    access_token = create_access_token(data=access_token_data, expires_delta=access_token_expires)

    refresh_token_data = {
        "sub": user.email,
        "id": str(user.id),
    }
    refresh_token = create_refresh_token(data=refresh_token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }

