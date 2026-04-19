"""Comment service layer."""

from uuid import UUID
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.comment_repository import create_comment, get_comments_by_ticket, get_comment_by_id, update_comment, delete_comment
from app.repositories.ticket_repository import get_ticket_by_id
from app.repositories.project_member_repository import get_project_member_by_user_and_project
from app.schemas.comment_schemas import CommentCreate, CommentUpdate, CommentResponse
from app.schemas.response_schemas import APIResponse
from app.constant.role_constant import ROLE_ADMIN, ROLE_PROJECT_MANAGER, ROLE_DEVELOPER, ROLE_REPORTER
from app.constant.comment_constant import (
    ERROR_COMMENT_NOT_FOUND, ERROR_COMMENT_FORBIDDEN, ERROR_COMMENT_UPDATE_FORBIDDEN, ERROR_COMMENT_DELETE_FORBIDDEN,
    SUCCESS_COMMENT_CREATED, SUCCESS_COMMENT_UPDATED, SUCCESS_COMMENT_DELETED, SUCCESS_COMMENTS_FETCHED
)


class CommentService:
    """Provides comment business logic."""

    def __init__(self, db: AsyncSession):
        """Initialize the service.

        Args:
            db: Database session.
        """
        self.db = db

    async def _assert_ticket_exists(self, ticket_id: UUID):
        """Validate that a ticket exists.

        Args:
            ticket_id: Ticket identifier.

        Returns:
            Any: Matching ticket record.

        Raises:
            HTTPException: If the ticket does not exist.
        """
        ticket = await get_ticket_by_id(self.db, ticket_id)
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_COMMENT_FORBIDDEN)  # Using existing constant
        return ticket

    async def _assert_member_has_access(self, ticket, current_user: dict):
        """Validate that the user can access the ticket's project.

        Args:
            ticket: Ticket record.
            current_user: Authenticated user payload.

        Raises:
            HTTPException: If the user does not have access.
        """
        if current_user.get("role") == ROLE_ADMIN:
            if str(ticket.project.organization_id) != current_user.get("organization_id"):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_COMMENT_FORBIDDEN)
            return

        user_id = UUID(current_user.get("id"))
        project_member = await get_project_member_by_user_and_project(self.db, user_id, ticket.project_id)
        if not project_member or not project_member.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_COMMENT_FORBIDDEN)

    async def _assert_comment_exists(self, comment_id: UUID):
        """Validate that a comment exists.

        Args:
            comment_id: Comment identifier.

        Returns:
            Any: Matching comment record.

        Raises:
            HTTPException: If the comment does not exist.
        """
        comment = await get_comment_by_id(self.db, comment_id)
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_COMMENT_NOT_FOUND)
        return comment

    async def _assert_comment_permission(self, comment, current_user: dict, action: str):
        """Validate that the user can modify a comment.

        Args:
            comment: Comment record.
            current_user: Authenticated user payload.
            action: Requested action name.

        Raises:
            HTTPException: If the user is not allowed to perform the action.
        """
        role = current_user.get("role")

        if role in [ROLE_DEVELOPER, ROLE_REPORTER]:
            # Can only modify their own comments
            user_id = UUID(current_user.get("id"))
            if str(comment.created_by) != str(user_id):
                if action == "update":
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_COMMENT_UPDATE_FORBIDDEN)
                elif action == "delete":
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_COMMENT_DELETE_FORBIDDEN)

    async def get_comments_by_ticket_service(self, ticket_id: UUID, current_user: dict, skip: int = 0, limit: int = 100) -> APIResponse[List[CommentResponse]]:
        """Get comments for a ticket.

        Args:
            ticket_id: Ticket identifier.
            current_user: Authenticated user payload.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            APIResponse[List[CommentResponse]]: Comment list response.
        """
        ticket = await self._assert_ticket_exists(ticket_id)
        await self._assert_member_has_access(ticket, current_user)
        comments = await get_comments_by_ticket(self.db, ticket_id, skip, limit)
        return APIResponse.success_response(SUCCESS_COMMENTS_FETCHED, [CommentResponse.model_validate(comment) for comment in comments])

    async def create_comment_service(self, ticket_id: UUID, comment_data: CommentCreate, current_user: dict) -> APIResponse[CommentResponse]:
        """Create a comment.

        Args:
            ticket_id: Ticket identifier.
            comment_data: Comment creation payload.
            current_user: Authenticated user payload.

        Returns:
            APIResponse[CommentResponse]: Comment creation response.
        """
        ticket = await self._assert_ticket_exists(ticket_id)
        await self._assert_member_has_access(ticket, current_user)

        user_id = UUID(current_user.get("id"))
        project_member = await get_project_member_by_user_and_project(self.db, user_id, ticket.project_id)
        if not project_member or not project_member.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_COMMENT_FORBIDDEN)

        payload = comment_data.model_dump(exclude_none=True)
        payload["ticket_id"] = ticket_id
        payload["project_id"] = ticket.project_id
        payload["created_by"] = project_member.id

        comment = await create_comment(self.db, payload)
        return APIResponse.success_response(SUCCESS_COMMENT_CREATED, CommentResponse.model_validate(comment))

    async def update_comment_service(self, comment_id: UUID, comment_data: CommentUpdate, current_user: dict) -> APIResponse[CommentResponse]:
        """Update a comment.

        Args:
            comment_id: Comment identifier.
            comment_data: Comment update payload.
            current_user: Authenticated user payload.

        Returns:
            APIResponse[CommentResponse]: Comment update response.
        """
        comment = await self._assert_comment_exists(comment_id)
        await self._assert_comment_permission(comment, current_user, "update")

        user_id = UUID(current_user.get("id"))
        project_member = await get_project_member_by_user_and_project(self.db, user_id, comment.project_id)
        if not project_member or not project_member.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_COMMENT_FORBIDDEN)

        update_data = comment_data.model_dump(exclude_none=True)
        update_data["updated_by"] = project_member.id

        updated_comment = await update_comment(self.db, comment_id, update_data)
        return APIResponse.success_response(SUCCESS_COMMENT_UPDATED, CommentResponse.model_validate(updated_comment))

    async def delete_comment_service(self, comment_id: UUID, current_user: dict) -> APIResponse[dict]:
        """Delete a comment.

        Args:
            comment_id: Comment identifier.
            current_user: Authenticated user payload.

        Returns:
            APIResponse[dict]: Comment deletion response.
        """
        comment = await self._assert_comment_exists(comment_id)
        await self._assert_comment_permission(comment, current_user, "delete")

        user_id = UUID(current_user.get("id"))
        project_member = await get_project_member_by_user_and_project(self.db, user_id, comment.project_id)
        if not project_member or not project_member.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_COMMENT_FORBIDDEN)

        await delete_comment(self.db, comment_id, project_member.id)
        return APIResponse.success_response(SUCCESS_COMMENT_DELETED, {"message": "Comment deleted successfully"})
