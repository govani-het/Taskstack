"""Dashboard API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List

from app.authentication.role_base_auth_token import get_current_user
from app.config.database import get_db
from app.schemas.response_schemas import APIResponse
from app.schemas.dashboard_schemas import DashboardSummary
from app.schemas.ticket_schemas import TicketResponse
from app.services.dashboard_service import DashboardService
from app.utils.access_control import require_roles
from app.constant.role_constant import ROLE_ADMIN, ROLE_PROJECT_MANAGER

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
)

# Only admins and project managers can access dashboard
ALLOWED_ROLES = [ROLE_ADMIN, ROLE_PROJECT_MANAGER]


@router.get("/summary", response_model=APIResponse[DashboardSummary])
@require_roles(ALLOWED_ROLES)
async def get_dashboard_summary(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)]
):
    """Get dashboard summary with overall project tracking metrics.

    Returns overall statistics for projects accessible to the current user.
    - Project Managers: See metrics for projects where they are assigned as project manager
    - Admins: See metrics for all projects in their organization

    Args:
        db: Database session dependency.
        current_user: Authenticated user payload (injected by require_roles).

    Returns:
        APIResponse containing dashboard summary statistics.
    """
    service = DashboardService(db)
    return await service.get_dashboard_summary_service(current_user)


@router.get("/pending-issues", response_model=APIResponse[List[TicketResponse]])
@require_roles(ALLOWED_ROLES)
async def get_pending_issues(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],  # Will be injected by require_roles
    skip: int = 0,
    limit: int = 100,
):
    """Get pending issues (tickets with status 'pending' or 'process').

    Returns tickets from projects accessible to the current user.
    - Project Managers: See tickets from projects where they are assigned as project manager
    - Admins: See tickets from all projects in their organization

    Args:
        db: Database session dependency.
        current_user: Authenticated user payload (injected by require_roles).
        skip: Number of records to skip for pagination.
        limit: Maximum number of records to return.

    Returns:
        APIResponse containing list of pending tickets.
    """
    service = DashboardService(db)
    return await service.get_pending_issues_service(current_user, skip, limit)


@router.get("/completed-tasks", response_model=APIResponse[List[TicketResponse]])
@require_roles(ALLOWED_ROLES)
async def get_completed_tasks(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],  # Will be injected by require_roles
    skip: int = 0,
    limit: int = 100,
):
    """Get completed tasks (tickets with status 'completed').

    Returns tickets from projects accessible to the current user.
    - Project Managers: See tickets from projects where they are assigned as project manager
    - Admins: See tickets from all projects in their organization

    Args:
        db: Database session dependency.
        current_user: Authenticated user payload (injected by require_roles).
        skip: Number of records to skip for pagination.
        limit: Maximum number of records to return.

    Returns:
        APIResponse containing list of completed tickets.
    """
    service = DashboardService(db)
    return await service.get_completed_tasks_service(current_user, skip, limit)
