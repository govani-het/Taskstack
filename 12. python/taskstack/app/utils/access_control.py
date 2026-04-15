from fastapi import HTTPException, status, Depends
from typing import Iterable, Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.role_base_auth_token import get_current_user


def require_roles(allowed_roles: list[str]):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )

        return user

    return role_checker