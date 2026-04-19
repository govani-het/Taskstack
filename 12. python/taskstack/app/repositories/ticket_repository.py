"""Ticket repository functions."""

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.models.ticket import Ticket
from app.models.project_member import ProjectMember
from app.models.users import User
from app.models.roles import Role


async def get_ticket_by_id(db: AsyncSession, ticket_id: UUID) -> Optional[Ticket]:
    """Fetch an active ticket by ID with related data.

    Args:
        db: Database session.
        ticket_id: Ticket identifier.

    Returns:
        Optional[Ticket]: Matching active ticket, if found.
    """
    stmt = (
        select(Ticket)
        .options(
            selectinload(Ticket.project),
            selectinload(Ticket.created_by_member).selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(Ticket.assignee_member).selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(Ticket.updated_by_member).selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(Ticket.resolved_by_member).selectinload(ProjectMember.user).selectinload(User.role),
        )
        .where(Ticket.id == ticket_id, Ticket.is_active == True)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_tickets_by_project(db: AsyncSession, project_id: UUID, skip: int = 0, limit: int = 100) -> List[Ticket]:
    """Fetch active tickets for a project.

    Args:
        db: Database session.
        project_id: Project identifier.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        List[Ticket]: Active tickets for the project.
    """
    stmt = (
        select(Ticket)
        .options(
            selectinload(Ticket.created_by_member).selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(Ticket.assignee_member).selectinload(ProjectMember.user).selectinload(User.role),
        )
        .where(Ticket.project_id == project_id, Ticket.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_ticket(db: AsyncSession, ticket_data: dict) -> Ticket:
    """Create a ticket record.

    Args:
        db: Database session.
        ticket_data: Ticket field values.

    Returns:
        Ticket: Newly created ticket with related data loaded.
    """
    ticket = Ticket(**ticket_data)
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    stmt = (
        select(Ticket)
        .options(
            selectinload(Ticket.created_by_member).selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(Ticket.assignee_member).selectinload(ProjectMember.user).selectinload(User.role),
        )
        .where(Ticket.id == ticket.id)
    )
    result = await db.execute(stmt)
    return result.scalar_one()


async def update_ticket(db: AsyncSession, ticket: Ticket, update_data: dict) -> Ticket:
    """Update a ticket record.

    Args:
        db: Database session.
        ticket: Ticket instance to update.
        update_data: Fields to update.

    Returns:
        Ticket: Updated ticket with related data loaded.
    """
    for key, value in update_data.items():
        if hasattr(ticket, key):
            setattr(ticket, key, value)

    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    stmt = (
        select(Ticket)
        .options(
            selectinload(Ticket.created_by_member).selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(Ticket.assignee_member).selectinload(ProjectMember.user).selectinload(User.role),
        )
        .where(Ticket.id == ticket.id)
    )
    result = await db.execute(stmt)
    return result.scalar_one()


async def delete_ticket(db: AsyncSession, ticket: Ticket, deleted_by_id: UUID) -> Ticket:
    """Soft-delete a ticket with audit tracking.

    Args:
        db: Database session.
        ticket: Ticket instance to delete.
        deleted_by_id: Identifier of the user deleting the ticket.

    Returns:
        Ticket: Soft-deleted ticket with related data loaded.
    """
    from datetime import datetime, timezone
    from app.models.project_member import ProjectMember as PM
    
    ticket.is_active = False
    ticket.deleted_by = deleted_by_id
    ticket.deleted_at = datetime.now(timezone.utc)
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    stmt = (
        select(Ticket)
        .options(
            selectinload(Ticket.created_by_member).selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(Ticket.assignee_member).selectinload(ProjectMember.user).selectinload(User.role),
        )
        .where(Ticket.id == ticket.id)
    )
    result = await db.execute(stmt)
    return result.scalar_one()
