"""Dashboard service layer."""

from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.dashboard_repository import (
    get_accessible_project_ids,
    get_dashboard_summary,
    get_pending_tickets,
    get_completed_tickets,
)
from app.schemas.dashboard_schemas import DashboardSummary
from app.schemas.ticket_schemas import TicketResponse
from app.schemas.response_schemas import APIResponse
from app.constant.dashboard_constant import (
    ERROR_DASHBOARD_ACCESS_DENIED,
    SUCCESS_DASHBOARD_SUMMARY_FETCHED,
    SUCCESS_PENDING_ISSUES_FETCHED,
    SUCCESS_COMPLETED_TASKS_FETCHED,
)
from app.constant.role_constant import ROLE_ADMIN, ROLE_PROJECT_MANAGER


class DashboardService:
    """Service for dashboard operations.

    Provides business logic for dashboard data retrieval with proper access control.
    """

    def __init__(self, db: AsyncSession):
        """Initialize service with database session.

        Args:
            db: Database session for data operations.
        """
        self.db = db

    async def get_dashboard_summary_service(self, current_user: dict) -> APIResponse[DashboardSummary]:
        """Get dashboard summary for the current user.

        Retrieves overall project tracking metrics for projects accessible to the user.
        Only admins and project managers can access this endpoint.

        Args:
            current_user: Authenticated user payload containing role and organization info.

        Returns:
            APIResponse containing dashboard summary statistics.

        Raises:
            HTTPException: If user doesn't have permission to access dashboard.
        """
        if current_user["role"] not in [ROLE_ADMIN, ROLE_PROJECT_MANAGER]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ERROR_DASHBOARD_ACCESS_DENIED,
            )

        project_ids = await get_accessible_project_ids(self.db, current_user)
        summary_data = await get_dashboard_summary(self.db, project_ids)

        return APIResponse.success_response(
            SUCCESS_DASHBOARD_SUMMARY_FETCHED,
            DashboardSummary(**summary_data)
        )

    async def get_pending_issues_service(
        self, current_user: dict, skip: int = 0, limit: int = 100
    ) -> APIResponse[List[TicketResponse]]:
        """Get pending issues for the current user.

        Retrieves tickets with 'pending' or 'process' status from accessible projects.
        Only admins and project managers can access this endpoint.

        Args:
            current_user: Authenticated user payload containing role and organization info.
            skip: Number of records to skip for pagination.
            limit: Maximum number of records to return.

        Returns:
            APIResponse containing list of pending tickets.

        Raises:
            HTTPException: If user doesn't have permission to access dashboard.
        """
        if current_user["role"] not in [ROLE_ADMIN, ROLE_PROJECT_MANAGER]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ERROR_DASHBOARD_ACCESS_DENIED,
            )

        project_ids = await get_accessible_project_ids(self.db, current_user)
        tickets = await get_pending_tickets(self.db, project_ids, skip, limit)

        return APIResponse.success_response(
            SUCCESS_PENDING_ISSUES_FETCHED,
            [TicketResponse.model_validate(ticket) for ticket in tickets]
        )

    async def get_completed_tasks_service(
        self, current_user: dict, skip: int = 0, limit: int = 100
    ) -> APIResponse[List[TicketResponse]]:
        """Get completed tasks for the current user.

        Retrieves tickets with 'completed' status from accessible projects.
        Only admins and project managers can access this endpoint.

        Args:
            current_user: Authenticated user payload containing role and organization info.
            skip: Number of records to skip for pagination.
            limit: Maximum number of records to return.

        Returns:
            APIResponse containing list of completed tickets.

        Raises:
            HTTPException: If user doesn't have permission to access dashboard.
        """
        if current_user["role"] not in [ROLE_ADMIN, ROLE_PROJECT_MANAGER]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ERROR_DASHBOARD_ACCESS_DENIED,
            )

        project_ids = await get_accessible_project_ids(self.db, current_user)
        tickets = await get_completed_tickets(self.db, project_ids, skip, limit)

        return APIResponse.success_response(
            SUCCESS_COMPLETED_TASKS_FETCHED,
            [TicketResponse.model_validate(ticket) for ticket in tickets]
        )