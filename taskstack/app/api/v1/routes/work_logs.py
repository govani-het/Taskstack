"""Work log API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List, Optional
from uuid import UUID

from app.config.database import get_db
from app.schemas.response_schemas import APIResponse
from app.schemas.work_log_schemas import WorkLogCreate, WorkLogUpdate, WorkLogResponse
from app.services.work_log_service import WorkLogService
from app.authentication.role_base_auth_token import get_current_user
from app.utils.access_control import require_roles
from app.constant.role_constant import (
    ROLE_ADMIN,
    ROLE_DEVELOPER,
    ROLE_PROJECT_MANAGER,
    ROLE_REPORTER,
)

router = APIRouter(
    prefix="/work-logs",
    tags=["work logs"],
)

# Define role permissions for each operation
READ_ROLES = [ROLE_ADMIN, ROLE_PROJECT_MANAGER, ROLE_DEVELOPER, ROLE_REPORTER]
CREATE_ROLES = [ROLE_ADMIN, ROLE_PROJECT_MANAGER, ROLE_DEVELOPER, ROLE_REPORTER]
UPDATE_ROLES = [ROLE_ADMIN, ROLE_PROJECT_MANAGER, ROLE_DEVELOPER, ROLE_REPORTER]
DELETE_ROLES = [ROLE_ADMIN, ROLE_PROJECT_MANAGER, ROLE_DEVELOPER, ROLE_REPORTER]


@router.get("/", response_model=APIResponse[List[WorkLogResponse]])
@require_roles(READ_ROLES)
async def get_work_logs(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[UUID] = None,
    ticket_id: Optional[UUID] = None,
):
    """Get work logs based on user role and permissions.

    Args:
        db: Database session.
        current_user: Authenticated user payload.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
        project_id: Optional filter by project ID.
        ticket_id: Optional filter by ticket ID.

    Returns:
        APIResponse[List[WorkLogResponse]]: Work logs response.
    """
    work_log_service = WorkLogService(db)
    return await work_log_service.get_work_logs_service(
        current_user, skip, limit, project_id, ticket_id
    )


@router.get("/{work_log_id}", response_model=APIResponse[WorkLogResponse])
@require_roles(READ_ROLES)
async def get_work_log_by_id(
    work_log_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Get a specific work log by ID.

    Args:
        work_log_id: Work log identifier.
        db: Database session.
        current_user: Authenticated user payload.

    Returns:
        APIResponse[WorkLogResponse]: Work log response.
    """
    work_log_service = WorkLogService(db)
    return await work_log_service.get_work_log_by_id_service(work_log_id, current_user)


@router.post("/", response_model=APIResponse[WorkLogResponse])
@require_roles(CREATE_ROLES)
async def create_work_log(
    work_log_data: WorkLogCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Create a new work log.

    Args:
        work_log_data: Work log creation payload.
        db: Database session.
        current_user: Authenticated user payload.

    Returns:
        APIResponse[WorkLogResponse]: Work log creation response.
    """
    work_log_service = WorkLogService(db)
    return await work_log_service.create_work_log_service(work_log_data, current_user)


@router.patch("/{work_log_id}", response_model=APIResponse[WorkLogResponse])
@require_roles(UPDATE_ROLES)
async def update_work_log(
    work_log_id: UUID,
    work_log_data: WorkLogUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Update an existing work log.

    Args:
        work_log_id: Work log identifier.
        work_log_data: Work log update payload.
        db: Database session.
        current_user: Authenticated user payload.

    Returns:
        APIResponse[WorkLogResponse]: Work log update response.
    """
    work_log_service = WorkLogService(db)
    return await work_log_service.update_work_log_service(
        work_log_id, work_log_data, current_user
    )


@router.delete("/{work_log_id}", response_model=APIResponse[dict])
@require_roles(DELETE_ROLES)
async def delete_work_log(
    work_log_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Delete a work log.

    Args:
        work_log_id: Work log identifier.
        db: Database session.
        current_user: Authenticated user payload.

    Returns:
        APIResponse[dict]: Work log deletion response.
    """
    work_log_service = WorkLogService(db)
    return await work_log_service.delete_work_log_service(work_log_id, current_user)