"""Project member repository functions."""

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from datetime import datetime, timezone

from app.models.project_member import ProjectMember
from app.models.users import User
from app.models.projects import Project


async def get_project_members_by_project(db: AsyncSession, project_id: UUID, skip: int = 0, limit: int = 100) -> List[ProjectMember]:
    """Get project members.
    
    Args:
        db: Database session.
        project_id: Project identifier.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    
    Returns:
        List[ProjectMember]: Result of the operation.
    """
    stmt = (
        select(ProjectMember)
        .options(
            selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(ProjectMember.role),
            selectinload(ProjectMember.project_manager)
        )
        .where(ProjectMember.project_id == project_id, ProjectMember.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_all_project_members(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ProjectMember]:
    """Get all project members.
    
    Args:
        db: Database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
    
    Returns:
        List[ProjectMember]: Result of the operation.
    """
    stmt = (
        select(ProjectMember)
        .options(
            selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(ProjectMember.role),
            selectinload(ProjectMember.project).selectinload(Project.organization),
            selectinload(ProjectMember.project_manager)
        )
        .where(ProjectMember.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_project_member(db: AsyncSession, member_data: dict) -> ProjectMember:
    """Create a project member.
    
    Args:
        db: Database session.
        member_data: Project member creation payload.
    
    Returns:
        ProjectMember: The created project member.
    """
    project_member = ProjectMember(**member_data)
    db.add(project_member)
    await db.commit()
    await db.refresh(project_member)
    # Reload with relationships
    stmt = (
        select(ProjectMember)
        .options(
            selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(ProjectMember.role),
            selectinload(ProjectMember.project),
            selectinload(ProjectMember.project_manager)
        )
        .where(ProjectMember.id == project_member.id)
    )
    result = await db.execute(stmt)
    return result.scalar_one()


async def get_project_member_by_user_and_project(db: AsyncSession, user_id: UUID, project_id: UUID) -> ProjectMember | None:
    """Get a project member by user and project.
    
    Args:
        db: Database session.
        user_id: User identifier.
        project_id: Project identifier.
    
    Returns:
        ProjectMember | None: The project member or None if not found.
    """
    stmt = (
        select(ProjectMember)
        .where(
            ProjectMember.user_id == user_id,
            ProjectMember.project_id == project_id,
            ProjectMember.is_active == True
        )
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_project_member_by_id(db: AsyncSession, member_id: UUID) -> ProjectMember | None:
    """Get a project member by project member id."""
    stmt = (
        select(ProjectMember)
        .options(
            selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(ProjectMember.role),
            selectinload(ProjectMember.project),
            selectinload(ProjectMember.project_manager),
        )
        .where(ProjectMember.id == member_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_project_manager_member(db: AsyncSession, user_id: UUID, project_id: UUID) -> ProjectMember | None:
    """Get a project member where the user is the project manager.
    
    Args:
        db: Database session.
        user_id: User identifier (project manager).
        project_id: Project identifier.
    
    Returns:
        ProjectMember | None: The project member where user is project manager or None if not found.
    """
    stmt = (
        select(ProjectMember)
        .where(
            ProjectMember.project_id == project_id,
            ProjectMember.project_manager_id == user_id,
            ProjectMember.is_active == True
        )
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def remove_project_member(db: AsyncSession, existing_member: ProjectMember, deleted_by_id: UUID) -> ProjectMember:
    """Remove (soft delete) a project member.
    
    Args:
        db: Database session.
        existing_member: The project member to remove.
        deleted_by_id: ID of the user performing the deletion.
    
    Returns:
        ProjectMember: The removed project member.
    """
    existing_member.is_active = False
    existing_member.deleted_by = deleted_by_id
    existing_member.deleted_at = datetime.now(timezone.utc)
    db.add(existing_member)
    await db.commit()
    await db.refresh(existing_member)
    
    # Reload with relationships
    stmt = (
        select(ProjectMember)
        .options(
            selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(ProjectMember.role),
            selectinload(ProjectMember.project),
            selectinload(ProjectMember.project_manager)
        )
        .where(ProjectMember.id == existing_member.id)
    )
    result = await db.execute(stmt)
    return result.scalar_one()


async def update_project_member(db: AsyncSession, existing_member: ProjectMember, update_data: dict, updated_by_id: UUID) -> ProjectMember:
    """Update a project member with audit tracking.
    
    Args:
        db: Database session.
        existing_member: The project member to update.
        update_data: Dictionary containing fields to update.
        updated_by_id: ID of the user performing the update.
    
    Returns:
        ProjectMember: The updated project member.
    """
    for key, value in update_data.items():
        if hasattr(existing_member, key):
            setattr(existing_member, key, value)
    
    existing_member.updated_by = updated_by_id
    db.add(existing_member)
    await db.commit()
    await db.refresh(existing_member)
    
    # Reload with relationships
    stmt = (
        select(ProjectMember)
        .options(
            selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(ProjectMember.role),
            selectinload(ProjectMember.project),
            selectinload(ProjectMember.project_manager)
        )
        .where(ProjectMember.id == existing_member.id)
    )
    result = await db.execute(stmt)
    return result.scalar_one()
