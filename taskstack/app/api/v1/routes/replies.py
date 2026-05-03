"""Reply API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from uuid import UUID

from app.config.database import get_db
from app.schemas.response_schemas import APIResponse
from app.schemas.reply_schemas import ReplyCreate, ReplyUpdate, ReplyResponse
from app.services.reply_service import ReplyService
from app.authentication.role_base_auth_token import get_current_user
from app.utils.access_control import require_roles
from app.constant.role_constant import (
    ROLE_ADMIN,
    ROLE_DEVELOPER,
    ROLE_PROJECT_MANAGER,
    ROLE_REPORTER,
)

router = APIRouter(
    prefix="/replies",
    tags=["replies"],
)

READ_ROLES = [ROLE_ADMIN, ROLE_PROJECT_MANAGER, ROLE_DEVELOPER, ROLE_REPORTER]
CREATE_ROLES = [ROLE_ADMIN, ROLE_PROJECT_MANAGER, ROLE_DEVELOPER, ROLE_REPORTER]
UPDATE_ROLES = [ROLE_ADMIN, ROLE_PROJECT_MANAGER, ROLE_DEVELOPER, ROLE_REPORTER]
DELETE_ROLES = [ROLE_ADMIN, ROLE_PROJECT_MANAGER, ROLE_DEVELOPER, ROLE_REPORTER]


@router.get("/comment/{comment_id}", response_model=APIResponse[List[ReplyResponse]])
@require_roles(READ_ROLES)
async def get_replies_by_comment(
    comment_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
):
    """Get replies for a comment.

    Args:
        comment_id: Comment identifier.
        db: Database session.
        current_user: Authenticated user payload.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        APIResponse[List[ReplyResponse]]: Reply list response.
    """
    reply_service = ReplyService(db)
    return await reply_service.get_replies_by_comment_service(comment_id, current_user, skip, limit)


@router.post("/comment/{comment_id}", response_model=APIResponse[ReplyResponse])
@require_roles(CREATE_ROLES)
async def create_reply(
    comment_id: UUID,
    reply_data: ReplyCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Create a reply for a comment.

    Args:
        comment_id: Comment identifier.
        reply_data: Reply creation payload.
        db: Database session.
        current_user: Authenticated user payload.

    Returns:
        APIResponse[ReplyResponse]: Reply creation response.
    """
    reply_service = ReplyService(db)
    return await reply_service.create_reply_service(comment_id, reply_data, current_user)


@router.patch("/{reply_id}", response_model=APIResponse[ReplyResponse])
@require_roles(UPDATE_ROLES)
async def update_reply(
    reply_id: UUID,
    reply_data: ReplyUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Update an existing reply.

    Args:
        reply_id: Reply identifier.
        reply_data: Reply update payload.
        db: Database session.
        current_user: Authenticated user payload.

    Returns:
        APIResponse[ReplyResponse]: Reply update response.
    """
    reply_service = ReplyService(db)
    return await reply_service.update_reply_service(reply_id, reply_data, current_user)


@router.delete("/{reply_id}", response_model=APIResponse[dict])
@require_roles(DELETE_ROLES)
async def delete_reply(
    reply_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Delete a reply.

    Args:
        reply_id: Reply identifier.
        db: Database session.
        current_user: Authenticated user payload.

    Returns:
        APIResponse[dict]: Reply deletion response.
    """
    reply_service = ReplyService(db)
    return await reply_service.delete_reply_service(reply_id, current_user)
