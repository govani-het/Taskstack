"""Ticket service layer."""

from uuid import UUID
from typing import List, Optional
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project_member import ProjectMember
from app.repositories.ticket_repository import (
    create_ticket,
    get_ticket_by_id,
    get_tickets_by_project,
    update_ticket,
    delete_ticket,
)
from app.repositories.project_repository import get_project_by_id
from app.repositories.project_member_repository import (
    get_project_member_by_id,
    get_project_member_by_user_and_project,
    get_project_manager_member,
)
from app.schemas.ticket_schemas import TicketCreate, TicketResponse, TicketUpdate
from app.schemas.response_schemas import APIResponse
from app.constant.role_constant import (
    ROLE_ADMIN,
    ROLE_DEVELOPER,
    ROLE_PROJECT_MANAGER,
    ROLE_REPORTER,
)
from app.constant.ticket_constant import (
    ERROR_ASSIGNEE_INVALID,
    ERROR_PROJECT_NOT_FOUND,
    ERROR_TICKET_ASSIGNMENT_NOT_ALLOWED,
    ERROR_TICKET_ASSIGN_NOT_ALLOWED,
    ERROR_TICKET_FORBIDDEN,
    ERROR_TICKET_NOT_FOUND,
    ERROR_TICKET_STATUS_CHANGE_NOT_ALLOWED,
    ERROR_TICKET_UPDATE_NOT_ALLOWED,
    ERROR_TICKET_DELETE_NOT_ALLOWED,
    SUCCESS_TICKET_CREATED,
    SUCCESS_TICKET_FETCHED,
    SUCCESS_TICKETS_FETCHED,
    SUCCESS_TICKET_UPDATED,
    SUCCESS_TICKET_DELETED,
    SUCCESS_TICKET_ASSIGNED,
    PRIORITY_HIGH,
    PRIORITY_INTERMEDIATE,
    PRIORITY_LOW,
    STATUS_PENDING,
    STATUS_PROCESS,
    STATUS_COMPLETED,
    STATUS_CANCELED,
)


ALLOWED_ASSIGNABLE_ROLES = {ROLE_DEVELOPER, ROLE_REPORTER}
ALLOWED_STATUS_VALUES = {STATUS_PENDING, STATUS_PROCESS, STATUS_COMPLETED, STATUS_CANCELED}
ALLOWED_PRIORITY_VALUES = {PRIORITY_HIGH, PRIORITY_INTERMEDIATE, PRIORITY_LOW}


class TicketService:
    """Provides ticket business logic."""

    def __init__(self, db: AsyncSession):
        """Initialize the service.

        Args:
            db: Database session.
        """
        self.db = db

    async def _assert_project_exists(self, project_id: UUID):
        """Validate that a project exists.

        Args:
            project_id: Project identifier.

        Returns:
            Any: Matching project record.

        Raises:
            HTTPException: If the project does not exist.
        """
        project = await get_project_by_id(self.db, project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_PROJECT_NOT_FOUND)
        return project

    async def _assert_project_member(self, project_id: UUID, user_id: UUID) -> ProjectMember:
        """Validate that a user is an active project member.

        Args:
            project_id: Project identifier.
            user_id: User identifier.

        Returns:
            ProjectMember: Active project membership.

        Raises:
            HTTPException: If the user is not an active member.
        """
        project_member = await get_project_member_by_user_and_project(self.db, user_id, project_id)
        if not project_member or not project_member.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_TICKET_FORBIDDEN)
        return project_member

    async def _assert_same_organization(self, project, organization_id: Optional[str]):
        """Validate that a project belongs to the given organization.

        Args:
            project: Project record.
            organization_id: Organization identifier from the current user.

        Raises:
            HTTPException: If the project belongs to a different organization.
        """
        if not organization_id or str(project.organization_id) != organization_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_TICKET_FORBIDDEN)

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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ERROR_TICKET_NOT_FOUND)
        return ticket

    async def _assert_assignable_member(self, assignee_id: UUID, project_id: UUID) -> ProjectMember:
        """Validate that a project member can be assigned to a ticket.

        Args:
            assignee_id: Project member identifier.
            project_id: Project identifier.

        Returns:
            ProjectMember: Assignable project member record.

        Raises:
            HTTPException: If the assignee is invalid.
        """
        assignee_member = await get_project_member_by_id(self.db, assignee_id)
        if not assignee_member or not assignee_member.is_active or str(assignee_member.project_id) != str(project_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERROR_ASSIGNEE_INVALID)

        if not assignee_member.user or not assignee_member.user.role:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERROR_ASSIGNEE_INVALID)

        if assignee_member.user.role.name not in ALLOWED_ASSIGNABLE_ROLES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERROR_ASSIGNEE_INVALID)

        return assignee_member

    async def get_tickets_by_project_service(self, project_id: UUID, current_user: dict, skip: int = 0, limit: int = 100) -> APIResponse[List[TicketResponse]]:
        """Get tickets for a project.

        Args:
            project_id: Project identifier.
            current_user: Authenticated user payload.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            APIResponse[List[TicketResponse]]: Ticket list response.
        """
        project = await self._assert_project_exists(project_id)
        role = current_user.get("role")
        user_id = UUID(current_user.get("id"))
        organization_id = current_user.get("organization_id")

        if role == ROLE_ADMIN:
            await self._assert_same_organization(project, organization_id)
        else:
            await self._assert_project_member(project_id, user_id)

        tickets = await get_tickets_by_project(self.db, project_id, skip, limit)
        return APIResponse.success_response(SUCCESS_TICKETS_FETCHED, [TicketResponse.model_validate(ticket) for ticket in tickets])

    async def get_ticket_service(self, ticket_id: UUID, current_user: dict) -> APIResponse[TicketResponse]:
        """Get a ticket by ID.

        Args:
            ticket_id: Ticket identifier.
            current_user: Authenticated user payload.

        Returns:
            APIResponse[TicketResponse]: Ticket lookup response.
        """
        ticket = await self._assert_ticket_exists(ticket_id)
        role = current_user.get("role")
        user_id = UUID(current_user.get("id"))
        organization_id = current_user.get("organization_id")

        if role == ROLE_ADMIN:
            await self._assert_same_organization(ticket.project, organization_id)
        else:
            await self._assert_project_member(ticket.project_id, user_id)

        return APIResponse.success_response(SUCCESS_TICKET_FETCHED, TicketResponse.model_validate(ticket))

    async def create_ticket_service(self, ticket_data: TicketCreate, project_id: UUID, current_user: dict) -> APIResponse[TicketResponse]:
        """Create a ticket.

        Args:
            ticket_data: Ticket creation payload.
            project_id: Project identifier.
            current_user: Authenticated user payload.

        Returns:
            APIResponse[TicketResponse]: Ticket creation response.
        """
        project = await self._assert_project_exists(project_id)
        role = current_user.get("role")
        user_id = UUID(current_user.get("id"))
        organization_id = current_user.get("organization_id")

        if role == ROLE_ADMIN:
            await self._assert_same_organization(project, organization_id)
        else:
            creator_member = await self._assert_project_member(project_id, user_id)

        payload = ticket_data.model_dump(exclude_none=True)
        payload.setdefault("status", STATUS_PENDING)
        payload.setdefault("priority", PRIORITY_INTERMEDIATE)
        payload["project_id"] = project_id

        if role not in [ROLE_ADMIN, ROLE_PROJECT_MANAGER] and payload.get("status") != STATUS_PENDING:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_TICKET_STATUS_CHANGE_NOT_ALLOWED)

        if payload.get("assignee_id") is not None and role not in [ROLE_ADMIN, ROLE_PROJECT_MANAGER]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_TICKET_ASSIGNMENT_NOT_ALLOWED)

        if payload.get("assignee_id") is not None:
            assignee_member = await self._assert_assignable_member(payload["assignee_id"], project_id)
            payload["assignee_id"] = assignee_member.id

        if role == ROLE_ADMIN:
            owner_member = await self._assert_project_member(project_id, user_id)
        else:
            owner_member = creator_member

        payload["created_by"] = owner_member.id
        ticket = await create_ticket(self.db, payload)
        return APIResponse.success_response(SUCCESS_TICKET_CREATED, TicketResponse.model_validate(ticket))

    async def update_ticket_service(self, ticket_id: UUID, ticket_data: TicketUpdate, current_user: dict) -> APIResponse[TicketResponse]:
        """Update a ticket.

        Args:
            ticket_id: Ticket identifier.
            ticket_data: Ticket update payload.
            current_user: Authenticated user payload.

        Returns:
            APIResponse[TicketResponse]: Ticket update response.
        """
        ticket = await self._assert_ticket_exists(ticket_id)
        role = current_user.get("role")
        user_id = UUID(current_user.get("id"))
        organization_id = current_user.get("organization_id")

        if role == ROLE_ADMIN:
            await self._assert_same_organization(ticket.project, organization_id)
        elif role == ROLE_PROJECT_MANAGER:
            await self._assert_project_manager(ticket.project_id, user_id)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_TICKET_UPDATE_NOT_ALLOWED)

        update_payload = ticket_data.model_dump(exclude_none=True)
        if not update_payload:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided to update")

        if update_payload.get("assignee_id") is not None:
            assignee_member = await self._assert_assignable_member(update_payload["assignee_id"], ticket.project_id)
            update_payload["assignee_id"] = assignee_member.id

        if update_payload.get("status") is not None and role != ROLE_PROJECT_MANAGER and role != ROLE_ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_TICKET_STATUS_CHANGE_NOT_ALLOWED)

        if update_payload.get("status") is not None and update_payload["status"] not in ALLOWED_STATUS_VALUES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid status value: {update_payload['status']}")

        if update_payload.get("priority") is not None and update_payload["priority"] not in ALLOWED_PRIORITY_VALUES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid priority value: {update_payload['priority']}")

        update_payload["updated_by"] = user_id
        updated_ticket = await update_ticket(self.db, ticket, update_payload)
        return APIResponse.success_response(SUCCESS_TICKET_UPDATED, TicketResponse.model_validate(updated_ticket))

    async def delete_ticket_service(self, ticket_id: UUID, current_user: dict) -> APIResponse[TicketResponse]:
        """Delete a ticket.

        Args:
            ticket_id: Ticket identifier.
            current_user: Authenticated user payload.

        Returns:
            APIResponse[TicketResponse]: Ticket deletion response.
        """
        ticket = await self._assert_ticket_exists(ticket_id)
        role = current_user.get("role")
        user_id = UUID(current_user.get("id"))
        organization_id = current_user.get("organization_id")

        # Admin can delete any ticket in their organization
        if role == ROLE_ADMIN:
            await self._assert_same_organization(ticket.project, organization_id)
        # Project Manager can delete tickets from projects they manage
        elif role == ROLE_PROJECT_MANAGER:
            await self._assert_project_manager(ticket.project_id, user_id)
        # Reporter can only delete their own tickets
        elif role == ROLE_REPORTER:
            if not ticket.created_by_member or str(ticket.created_by_member.user_id) != str(user_id):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_TICKET_DELETE_NOT_ALLOWED)
        else:
            # DEVELOPER or others cannot delete
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_TICKET_DELETE_NOT_ALLOWED)

        # Get user's project member record for audit trail
        user_project_member = await get_project_member_by_user_and_project(self.db, user_id, ticket.project_id)
        if not user_project_member:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_TICKET_DELETE_NOT_ALLOWED)

        deleted_ticket = await delete_ticket(self.db, ticket, user_project_member.id)
        return APIResponse.success_response(SUCCESS_TICKET_DELETED, TicketResponse.model_validate(deleted_ticket))

    async def assign_ticket_service(self, ticket_id: UUID, assignee_id: UUID, current_user: dict) -> APIResponse[TicketResponse]:
        """Assign a ticket to a project member.

        Args:
            ticket_id: Ticket identifier.
            assignee_id: Project member identifier to assign the ticket to.
            current_user: Authenticated user payload.

        Returns:
            APIResponse[TicketResponse]: Ticket assignment response.
        """
        ticket = await self._assert_ticket_exists(ticket_id)
        role = current_user.get("role")
        user_id = UUID(current_user.get("id"))
        organization_id = current_user.get("organization_id")

        # Only admin and project manager can assign tickets
        if role == ROLE_ADMIN:
            await self._assert_same_organization(ticket.project, organization_id)
        elif role == ROLE_PROJECT_MANAGER:
            await self._assert_project_manager(ticket.project_id, user_id)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_TICKET_ASSIGN_NOT_ALLOWED)

        # Validate assignee
        assignee_member = await self._assert_assignable_member(assignee_id, ticket.project_id)

        # Update ticket with new assignee
        update_payload = {"assignee_id": assignee_member.id}
        user_project_member = await get_project_member_by_user_and_project(self.db, user_id, ticket.project_id)
        if user_project_member:
            update_payload["updated_by"] = user_project_member.id

        updated_ticket = await update_ticket(self.db, ticket, update_payload)
        return APIResponse.success_response(SUCCESS_TICKET_ASSIGNED, TicketResponse.model_validate(updated_ticket))

    async def _assert_project_manager(self, project_id: UUID, user_id: UUID) -> ProjectMember:
        """Validate that a user is the project manager for a project.

        Args:
            project_id: Project identifier.
            user_id: User identifier.

        Returns:
            ProjectMember: Project manager membership record.

        Raises:
            HTTPException: If the user is not the project manager.
        """
        project_manager_member = await get_project_manager_member(self.db, user_id, project_id)
        if not project_manager_member:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_TICKET_FORBIDDEN)
        return project_manager_member
