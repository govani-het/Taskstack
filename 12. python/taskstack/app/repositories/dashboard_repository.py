"""Dashboard repository."""

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.models.projects import Project
from app.models.ticket import Ticket
from app.models.project_member import ProjectMember
from app.models.users import User
from app.constant.role_constant import ROLE_ADMIN, ROLE_PROJECT_MANAGER


async def get_accessible_project_ids(db: AsyncSession, current_user: dict) -> List[UUID]:
    """Get project IDs accessible to the current user.

    For admins, returns all active projects in their organization.
    For project managers, returns distinct projects where they are assigned as project manager.
    For other roles, returns empty list.

    Args:
        db: Database session.
        current_user: Authenticated user payload containing role and organization_id.

    Returns:
        List of accessible project UUIDs.
    """
    if current_user["role"] == ROLE_ADMIN:
        query = select(Project.id).where(
            and_(Project.organization_id == current_user["organization_id"], Project.is_active == True)
        )
    elif current_user["role"] == ROLE_PROJECT_MANAGER:
        query = select(ProjectMember.project_id.distinct()).where(
            and_(ProjectMember.project_manager_id == current_user["id"], ProjectMember.is_active == True)
        ).join(Project, ProjectMember.project_id == Project.id).where(Project.is_active == True)
    else:
        # For other roles, return empty list or handle differently
        return []

    result = await db.execute(query)
    return [row[0] for row in result.fetchall()]


async def get_dashboard_summary(db: AsyncSession, project_ids: List[UUID]) -> dict:
    """Get dashboard summary statistics for given projects.

    Calculates various counts including projects, tickets by status, and members.

    Args:
        db: Database session.
        project_ids: List of project UUIDs to include in summary.

    Returns:
        Dictionary containing summary statistics with keys:
        - total_projects: Total number of projects
        - active_projects: Number of active projects
        - total_tickets: Total number of tickets
        - pending_tickets: Number of pending tickets
        - in_progress_tickets: Number of in-progress tickets
        - completed_tickets: Number of completed tickets
        - canceled_tickets: Number of canceled tickets
        - total_members: Total number of project members
        - active_members: Number of active project members
    """
    if not project_ids:
        return {
            "total_projects": 0,
            "active_projects": 0,
            "total_tickets": 0,
            "pending_tickets": 0,
            "in_progress_tickets": 0,
            "completed_tickets": 0,
            "canceled_tickets": 0,
            "total_members": 0,
            "active_members": 0,
        }

    # Total projects
    total_projects = len(project_ids)

    # Active projects (already filtered)
    active_projects = total_projects

    # Ticket counts
    ticket_query = select(
        func.count(Ticket.id).label("total"),
        func.sum(func.case((Ticket.status == "pending", 1), else_=0)).label("pending"),
        func.sum(func.case((Ticket.status == "process", 1), else_=0)).label("in_progress"),
        func.sum(func.case((Ticket.status == "completed", 1), else_=0)).label("completed"),
        func.sum(func.case((Ticket.status == "canceled", 1), else_=0)).label("canceled"),
    ).where(and_(Ticket.project_id.in_(project_ids), Ticket.is_active == True))

    ticket_result = await db.execute(ticket_query)
    ticket_counts = ticket_result.first()

    # Member counts
    member_query = select(
        func.count(ProjectMember.id).label("total"),
        func.sum(func.case((ProjectMember.is_active == True, 1), else_=0)).label("active"),
    ).where(and_(ProjectMember.project_id.in_(project_ids), ProjectMember.is_active == True))

    member_result = await db.execute(member_query)
    member_counts = member_result.first()

    return {
        "total_projects": total_projects,
        "active_projects": active_projects,
        "total_tickets": ticket_counts.total or 0,
        "pending_tickets": ticket_counts.pending or 0,
        "in_progress_tickets": ticket_counts.in_progress or 0,
        "completed_tickets": ticket_counts.completed or 0,
        "canceled_tickets": ticket_counts.canceled or 0,
        "total_members": member_counts.total or 0,
        "active_members": member_counts.active or 0,
    }


async def get_pending_tickets(db: AsyncSession, project_ids: List[UUID], skip: int = 0, limit: int = 100) -> List[Ticket]:
    """Get pending tickets from specified projects.

    Retrieves tickets with status 'pending' or 'process' that are active.

    Args:
        db: Database session.
        project_ids: List of project UUIDs to search in.
        skip: Number of records to skip for pagination.
        limit: Maximum number of records to return.

    Returns:
        List of Ticket objects with pending or in-progress status.
    """
    if not project_ids:
        return []

    query = select(Ticket).where(
        and_(
            Ticket.project_id.in_(project_ids),
            Ticket.status.in_(["pending", "process"]),
            Ticket.is_active == True
        )
    ).offset(skip).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


async def get_completed_tickets(db: AsyncSession, project_ids: List[UUID], skip: int = 0, limit: int = 100) -> List[Ticket]:
    """Get completed tickets from specified projects.

    Retrieves tickets with status 'completed' that are active.

    Args:
        db: Database session.
        project_ids: List of project UUIDs to search in.
        skip: Number of records to skip for pagination.
        limit: Maximum number of records to return.

    Returns:
        List of Ticket objects with completed status.
    """
    if not project_ids:
        return []

    query = select(Ticket).where(
        and_(
            Ticket.project_id.in_(project_ids),
            Ticket.status == "completed",
            Ticket.is_active == True
        )
    ).offset(skip).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()