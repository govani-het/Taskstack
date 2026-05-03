"""User API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated
from uuid import UUID

from app.config.database import get_db
from app.schemas.user_schemas import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService
from app.schemas.response_schemas import APIResponse
from app.authentication.role_base_auth_token import get_current_user

from app.constant.role_constant import ROLE_SYSTEM_ADMIN,ROLE_ADMIN,ROLE_DEVELOPER,ROLE_PROJECT_MANAGER,ROLE_REPORTER
from app.utils.access_control import require_roles

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=APIResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Create a user.

    Args:
        user_data: User creation payload.
        db: Database session.
    """
    user_obj = UserService(db)
    return await user_obj.create_user_service(user_data)


@router.get("/{user_id}", response_model=APIResponse[UserResponse])
@require_roles([ROLE_SYSTEM_ADMIN])
async def get_user(
    user_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Get a user by ID.

    Args:
        user_id: User identifier.
        db: Database session.
        current_user: Authenticated user payload.
    """
    user_obj = UserService(db)
    return await user_obj.get_user_service(user_id)


@router.get("/", response_model=APIResponse[List[UserResponse]])
@require_roles([ROLE_SYSTEM_ADMIN])
async def get_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,

):
    """Get users with pagination.

    Args:
        db: Database session.
        current_user: Authenticated user payload.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    """
    user_obj = UserService(db)
    return await user_obj.get_users_service(skip, limit)


@router.patch("/{user_id}", response_model=APIResponse[UserResponse])
@require_roles([ROLE_ADMIN,ROLE_DEVELOPER,ROLE_PROJECT_MANAGER,ROLE_REPORTER])
async def update_user(
    user_id: UUID,
    update_data: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Update a user.

    Args:
        user_id: User identifier.
        update_data: User update payload.
        db: Database session.
        current_user: Authenticated user payload.
    """
    user_obj = UserService(db)
    return await user_obj.update_user_service(user_id, update_data, UUID(current_user["id"]))


@router.delete("/{user_id}", response_model=APIResponse[str], status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Delete a user.

    Args:
        user_id: User identifier.
        db: Database session.
        current_user: Authenticated user payload.
    """
    user_obj = UserService(db)
    return await user_obj.delete_user_service(user_id, UUID(current_user["id"]))


@router.post("/{user_id}/promote-to-admin", response_model=APIResponse[UserResponse])
@require_roles([ROLE_ADMIN])
async def promote_to_admin(
    user_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Promote a user to admin role. Only admins can promote users.

    Args:
        user_id: User identifier to promote.
        db: Database session.
        current_user: Authenticated admin user.
    """
    user_obj = UserService(db)
    return await user_obj.promote_to_admin_service(user_id, current_user)
