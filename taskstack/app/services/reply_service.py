"""Reply service layer."""

from uuid import UUID
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.reply_repository import create_reply, get_replies_by_comment, get_reply_by_id, update_reply, delete_reply
from app.repositories.comment_repository import get_comment_by_id
from app.repositories.project_member_repository import get_project_member_by_user_and_project
from app.schemas.reply_schemas import ReplyCreate, ReplyUpdate, ReplyResponse
from app.schemas.response_schemas import APIResponse
from app.constant.role_constant import ROLE_ADMIN, ROLE_PROJECT_MANAGER, ROLE_DEVELOPER, ROLE_REPORTER
from app.constant.reply_constant import (
    ERROR_REPLY_NOT_FOUND, ERROR_REPLY_FORBIDDEN, ERROR_REPLY_UPDATE_FORBIDDEN, ERROR_REPLY_DELETE_FORBIDDEN,
    SUCCESS_REPLY_CREATED, SUCCESS_REPLY_UPDATED, SUCCESS_REPLY_DELETED, SUCCESS_REPLIES_FETCHED
)


class ReplyService:
    """Provides reply business logic."""

    def __init__(self, db: AsyncSession):
        """Initialize the service.

        Args:
            db: Database session.
        """
        self.db = db

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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_REPLY_FORBIDDEN)  # Using existing constant
        return comment

    async def _assert_member_has_access(self, comment, current_user: dict):
        """Validate that the user can access the reply's project.

        Args:
            comment: Comment record.
            current_user: Authenticated user payload.

        Raises:
            HTTPException: If the user does not have access.
        """
        if current_user.get("role") == ROLE_ADMIN:
            if str(comment.project.organization_id) != current_user.get("organization_id"):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_REPLY_FORBIDDEN)
            return

        user_id = UUID(current_user.get("id"))
        project_member = await get_project_member_by_user_and_project(self.db, user_id, comment.project_id)
        if not project_member or not project_member.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_REPLY_FORBIDDEN)

    async def _assert_reply_exists(self, reply_id: UUID):
        """Validate that a reply exists.

        Args:
            reply_id: Reply identifier.

        Returns:
            Any: Matching reply record.

        Raises:
            HTTPException: If the reply does not exist.
        """
        reply = await get_reply_by_id(self.db, reply_id)
        if not reply:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_REPLY_NOT_FOUND)
        return reply

    async def _assert_reply_permission(self, reply, current_user: dict, action: str):
        """Validate that the user can modify a reply.

        Args:
            reply: Reply record.
            current_user: Authenticated user payload.
            action: Requested action name.

        Raises:
            HTTPException: If the user is not allowed to perform the action.
        """
        role = current_user.get("role")

        if role in [ROLE_DEVELOPER, ROLE_REPORTER]:
            # Can only modify their own replies
            user_id = UUID(current_user.get("id"))
            if str(reply.created_by) != str(user_id):
                if action == "update":
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_REPLY_UPDATE_FORBIDDEN)
                elif action == "delete":
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_REPLY_DELETE_FORBIDDEN)

    async def get_replies_by_comment_service(self, comment_id: UUID, current_user: dict, skip: int = 0, limit: int = 100) -> APIResponse[List[ReplyResponse]]:
        """Get replies for a comment.

        Args:
            comment_id: Comment identifier.
            current_user: Authenticated user payload.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            APIResponse[List[ReplyResponse]]: Reply list response.
        """
        comment = await self._assert_comment_exists(comment_id)
        await self._assert_member_has_access(comment, current_user)
        replies = await get_replies_by_comment(self.db, comment_id, skip, limit)
        return APIResponse.success_response(SUCCESS_REPLIES_FETCHED, [ReplyResponse.model_validate(reply) for reply in replies])

    async def create_reply_service(self, comment_id: UUID, reply_data: ReplyCreate, current_user: dict) -> APIResponse[ReplyResponse]:
        """Create a reply.

        Args:
            comment_id: Comment identifier.
            reply_data: Reply creation payload.
            current_user: Authenticated user payload.

        Returns:
            APIResponse[ReplyResponse]: Reply creation response.
        """
        comment = await self._assert_comment_exists(comment_id)
        await self._assert_member_has_access(comment, current_user)

        user_id = UUID(current_user.get("id"))
        project_member = await get_project_member_by_user_and_project(self.db, user_id, comment.project_id)
        if not project_member or not project_member.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_REPLY_FORBIDDEN)

        payload = reply_data.model_dump(exclude_none=True)
        payload["comment_id"] = comment_id
        payload["project_id"] = comment.project_id
        payload["created_by"] = project_member.id

        reply = await create_reply(self.db, payload)
        return APIResponse.success_response(SUCCESS_REPLY_CREATED, ReplyResponse.model_validate(reply))

    async def update_reply_service(self, reply_id: UUID, reply_data: ReplyUpdate, current_user: dict) -> APIResponse[ReplyResponse]:
        """Update a reply.

        Args:
            reply_id: Reply identifier.
            reply_data: Reply update payload.
            current_user: Authenticated user payload.

        Returns:
            APIResponse[ReplyResponse]: Reply update response.
        """
        reply = await self._assert_reply_exists(reply_id)
        await self._assert_reply_permission(reply, current_user, "update")

        user_id = UUID(current_user.get("id"))
        project_member = await get_project_member_by_user_and_project(self.db, user_id, reply.project_id)
        if not project_member or not project_member.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_REPLY_FORBIDDEN)

        update_data = reply_data.model_dump(exclude_none=True)
        update_data["updated_by"] = project_member.id

        updated_reply = await update_reply(self.db, reply_id, update_data)
        return APIResponse.success_response(SUCCESS_REPLY_UPDATED, ReplyResponse.model_validate(updated_reply))

    async def delete_reply_service(self, reply_id: UUID, current_user: dict) -> APIResponse[dict]:
        """Delete a reply.

        Args:
            reply_id: Reply identifier.
            current_user: Authenticated user payload.

        Returns:
            APIResponse[dict]: Reply deletion response.
        """
        reply = await self._assert_reply_exists(reply_id)
        await self._assert_reply_permission(reply, current_user, "delete")

        user_id = UUID(current_user.get("id"))
        project_member = await get_project_member_by_user_and_project(self.db, user_id, reply.project_id)
        if not project_member or not project_member.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_REPLY_FORBIDDEN)

        await delete_reply(self.db, reply_id, project_member.id)
        return APIResponse.success_response(SUCCESS_REPLY_DELETED, {"message": "Reply deleted successfully"})
