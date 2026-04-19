"""Ticket API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from uuid import UUID

from app.config.database import get_db
from app.schemas.response_schemas import APIResponse
from app.schemas.ticket_schemas import TicketCreate, TicketResponse, TicketUpdate, TicketAssign
from app.schemas.comment_schemas import CommentCreate, CommentResponse
from app.services.ticket_service import TicketService
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
    prefix="/tickets",
    tags=["tickets"],
)

READ_ROLES = [ROLE_ADMIN, ROLE_PROJECT_MANAGER, ROLE_DEVELOPER, ROLE_REPORTER]
CREATE_ROLES = [ROLE_ADMIN, ROLE_PROJECT_MANAGER, ROLE_REPORTER]
UPDATE_ROLES = [ROLE_ADMIN, ROLE_PROJECT_MANAGER]
DELETE_ROLES = [ROLE_ADMIN, ROLE_PROJECT_MANAGER, ROLE_REPORTER]
COMMENT_ROLES = [ROLE_ADMIN, ROLE_PROJECT_MANAGER, ROLE_DEVELOPER, ROLE_REPORTER]


@router.get("/project/{project_id}", response_model=APIResponse[List[TicketResponse]])
@require_roles(READ_ROLES)
async def get_project_tickets(
    project_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
):
    """Get tickets for a project.

    Args:
        project_id: Project identifier.
        db: Database session.
        current_user: Authenticated user payload.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        APIResponse[List[TicketResponse]]: Ticket list response.
    """
    ticket_service = TicketService(db)
    return await ticket_service.get_tickets_by_project_service(project_id, current_user, skip, limit)


@router.get("/{ticket_id}", response_model=APIResponse[TicketResponse])
@require_roles(READ_ROLES)
async def get_ticket(
    ticket_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Get a ticket by ID.

    Args:
        ticket_id: Ticket identifier.
        db: Database session.
        current_user: Authenticated user payload.

    Returns:
        APIResponse[TicketResponse]: Ticket lookup response.
    """
    ticket_service = TicketService(db)
    return await ticket_service.get_ticket_service(ticket_id, current_user)


@router.post("/project/{project_id}", response_model=APIResponse[TicketResponse])
@require_roles(CREATE_ROLES)
async def create_ticket(
    ticket_data: TicketCreate,
    project_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Create a ticket in a project.

    Args:
        ticket_data: Ticket creation payload.
        project_id: Project identifier.
        db: Database session.
        current_user: Authenticated user payload.

    Returns:
        APIResponse[TicketResponse]: Ticket creation response.
    """
    ticket_service = TicketService(db)
    return await ticket_service.create_ticket_service(ticket_data, project_id, current_user)


@router.patch("/{ticket_id}", response_model=APIResponse[TicketResponse])
@require_roles(UPDATE_ROLES)
async def update_ticket(
    ticket_id: UUID,
    ticket_data: TicketUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Update a ticket.

    Args:
        ticket_id: Ticket identifier.
        ticket_data: Ticket update payload.
        db: Database session.
        current_user: Authenticated user payload.

    Returns:
        APIResponse[TicketResponse]: Ticket update response.
    """
    ticket_service = TicketService(db)
    return await ticket_service.update_ticket_service(ticket_id, ticket_data, current_user)


@router.delete("/{ticket_id}", response_model=APIResponse[TicketResponse])
@require_roles(DELETE_ROLES)
async def delete_ticket(
    ticket_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Delete a ticket.

    Args:
        ticket_id: Ticket identifier.
        db: Database session.
        current_user: Authenticated user payload.

    Returns:
        APIResponse[TicketResponse]: Ticket deletion response.
    """
    ticket_service = TicketService(db)
    return await ticket_service.delete_ticket_service(ticket_id, current_user)


@router.post("/{ticket_id}/assign", response_model=APIResponse[TicketResponse])
@require_roles([ROLE_ADMIN, ROLE_PROJECT_MANAGER])
async def assign_ticket(
    ticket_id: UUID,
    assignment_data: TicketAssign,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Assign a ticket to a project member.

    Args:
        ticket_id: Ticket identifier.
        assignment_data: Ticket assignment payload.
        db: Database session.
        current_user: Authenticated user payload.

    Returns:
        APIResponse[TicketResponse]: Ticket assignment response.
    """
    ticket_service = TicketService(db)
    return await ticket_service.assign_ticket_service(ticket_id, assignment_data.assignee_id, current_user)


@router.get("/{ticket_id}/comments", response_model=APIResponse[List[CommentResponse]])
@require_roles(COMMENT_ROLES)
async def get_ticket_comments(
    ticket_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Get comments for a ticket.

    Args:
        ticket_id: Ticket identifier.
        db: Database session.
        current_user: Authenticated user payload.

    Returns:
        APIResponse[List[CommentResponse]]: Comment list response.
    """
    comment_service = CommentService(db)
    return await comment_service.get_comments_by_ticket_service(ticket_id, current_user)


@router.post("/{ticket_id}/comments", response_model=APIResponse[CommentResponse])
@require_roles(COMMENT_ROLES)
async def add_ticket_comment(
    ticket_id: UUID,
    comment_data: CommentCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Add a comment to a ticket.

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
