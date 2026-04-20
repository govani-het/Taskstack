"""Work log service."""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status

from app.repositories.work_log_repository import (
    create_work_log,
    delete_work_log,
    get_work_log_by_id,
    get_work_logs,
    update_work_log,
)
from app.schemas.work_log_schemas import WorkLogCreate, WorkLogUpdate, WorkLogResponse
from app.schemas.response_schemas import APIResponse
from app.constant.work_log_constant import (
    SUCCESS_WORK_LOG_CREATED,
    SUCCESS_WORK_LOG_FETCHED,
    SUCCESS_WORK_LOGS_FETCHED,
    SUCCESS_WORK_LOG_UPDATED,
    SUCCESS_WORK_LOG_DELETED,
)


class WorkLogService:
    """Service for work log operations."""

    def __init__(self, db: AsyncSession):
        """Initialize service with database session."""
        self.db = db

    async def get_work_logs_service(
        self,
        current_user: dict,
        skip: int = 0,
        limit: int = 100,
        project_id: Optional[UUID] = None,
        ticket_id: Optional[UUID] = None,
    ) -> APIResponse[List[WorkLogResponse]]:
        """Get work logs for the current user based on their role."""
        try:
            work_logs = await get_work_logs(
                self.db, current_user, skip, limit, project_id, ticket_id
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(exc),
            )

        work_log_responses = [
            WorkLogResponse.model_validate(work_log) for work_log in work_logs
        ]

        return APIResponse(
            success=True,
            message=SUCCESS_WORK_LOGS_FETCHED,
            data=work_log_responses,
        )

    async def get_work_log_by_id_service(
        self, work_log_id: UUID, current_user: dict
    ) -> APIResponse[WorkLogResponse]:
        """Get a specific work log by ID."""
        try:
            work_log = await get_work_log_by_id(self.db, work_log_id, current_user)
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(exc),
            )

        work_log_response = WorkLogResponse.model_validate(work_log)

        return APIResponse(
            success=True,
            message=SUCCESS_WORK_LOG_FETCHED,
            data=work_log_response,
        )

    async def create_work_log_service(
        self, work_log_data: WorkLogCreate, current_user: dict
    ) -> APIResponse[WorkLogResponse]:
        """Create a new work log."""
        work_log_dict = work_log_data.model_dump()
        try:
            work_log = await create_work_log(self.db, work_log_dict, current_user)
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(exc),
            )

        work_log_response = WorkLogResponse.model_validate(work_log)

        return APIResponse(
            success=True,
            message=SUCCESS_WORK_LOG_CREATED,
            data=work_log_response,
        )

    async def update_work_log_service(
        self, work_log_id: UUID, work_log_data: WorkLogUpdate, current_user: dict
    ) -> APIResponse[WorkLogResponse]:
        """Update an existing work log."""
        update_dict = work_log_data.model_dump(exclude_unset=True)
        try:
            work_log = await update_work_log(
                self.db, work_log_id, update_dict, current_user
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(exc),
            )

        work_log_response = WorkLogResponse.model_validate(work_log)

        return APIResponse(
            success=True,
            message=SUCCESS_WORK_LOG_UPDATED,
            data=work_log_response,
        )

    async def delete_work_log_service(
        self, work_log_id: UUID, current_user: dict
    ) -> APIResponse[dict]:
        """Delete a work log."""
        try:
            await delete_work_log(self.db, work_log_id, current_user)
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(exc),
            )

        return APIResponse(
            success=True,
            message=SUCCESS_WORK_LOG_DELETED,
            data={"work_log_id": str(work_log_id)},
        )