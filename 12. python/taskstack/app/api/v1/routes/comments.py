"""Comment API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from uuid import UUID

from app.config.database import get_db
from app.schemas.response_schemas import APIResponse
from app.schemas.comment_schemas import CommentCreate, CommentUpdate, CommentResponse
from app.services.comment_service import CommentService
from app.authentication.role_base_auth_token import get_current_user
from app.utils.access_control import require_roles
from app.constant.role_constant import (
    ROLE_ADMIN,
    ROLE_DEVELOPER,
    ROLE_PROJECT_MANAGER,
    ROLE_REPORTER,
)

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)

READ_ROLES = [ROLE_ADMIN, ROLE_PROJECT_MANAGER, ROLE_DEVELOPER, ROLE_REPORTER]
CREATE_ROLES = [ROLE_ADMIN, ROLE_PROJECT_MANAGER, ROLE_DEVELOPER, ROLE_REPORTER]
UPDATE_ROLES = [ROLE_ADMIN, ROLE_PROJECT_MANAGER, ROLE_DEVELOPER, ROLE_REPORTER]
DELETE_ROLES = [ROLE_ADMIN, ROLE_PROJECT_MANAGER, ROLE_DEVELOPER, ROLE_REPORTER]


@router.get("/ticket/{ticket_id}", response_model=APIResponse[List[CommentResponse]])
@require_roles(READ_ROLES)
async def get_comments_by_ticket(
    ticket_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
):
    """Get comments for a ticket.

    Args:
        ticket_id: Ticket identifier.
        db: Database session.
        current_user: Authenticated user payload.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        APIResponse[List[CommentResponse]]: Comment list response.
    """
    comment_service = CommentService(db)
    return await comment_service.get_comments_by_ticket_service(ticket_id, current_user, skip, limit)


@router.post("/ticket/{ticket_id}", response_model=APIResponse[CommentResponse])
@require_roles(CREATE_ROLES)
async def create_comment(
    ticket_id: UUID,
    comment_data: CommentCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Create a comment for a ticket.

    Args:
        ticket_id: Ticket identifier.
        comment_data: Comment creation payload.
        db: Database session.
        current_user: Authenticated user payload.

    Returns:
        APIResponse[CommentResponse]: Comment creation response.
    """
    comment_service = CommentService(db)
    return await comment_service.create_comment_service(ticket_id, comment_data, current_user)


@router.patch("/{comment_id}", response_model=APIResponse[CommentResponse])
@require_roles(UPDATE_ROLES)
async def update_comment(
    comment_id: UUID,
    comment_data: CommentUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Update an existing comment.

    Args:
        comment_id: Comment identifier.
        comment_data: Comment update payload.
        db: Database session.
        current_user: Authenticated user payload.

    Returns:
        APIResponse[CommentResponse]: Comment update response.
    """
    comment_service = CommentService(db)
    return await comment_service.update_comment_service(comment_id, comment_data, current_user)


@router.delete("/{comment_id}", response_model=APIResponse[dict])
@require_roles(DELETE_ROLES)
async def delete_comment(
    comment_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Delete a comment.

    Args:
        comment_id: Comment identifier.
        db: Database session.
        current_user: Authenticated user payload.

    Returns:
        APIResponse[dict]: Comment deletion response.
    """
    comment_service = CommentService(db)
    return await comment_service.delete_comment_service(comment_id, current_user)
