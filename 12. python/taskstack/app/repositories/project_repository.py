"""Project repository functions."""

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone

from app.models.projects import Project
from app.models.project_member import ProjectMember
from app.models.users import User
from app.schemas.project_schemas import ProjectCreate


async def get_project_by_id(db: AsyncSession, project_id: UUID) -> Optional[Project]:
    """Fetch a project by ID.

    Args:
        db: Database session.
        project_id: Project identifier.

    Returns:
        Optional[Project]: Matching project, if found.
    """
    stmt = (
        select(Project)
        .options(
            selectinload(Project.organization),
            selectinload(Project.members).selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(Project.members).selectinload(ProjectMember.role)
        )
        .where(Project.id == project_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_projects_by_organization(db: AsyncSession, organization_id: UUID, skip: int = 0, limit: int = 100) -> List[Project]:
    """Fetch projects for an organization.

    Args:
        db: Database session.
        organization_id: Organization identifier.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        List[Project]: Projects belonging to the organization.
    """
    stmt = (
        select(Project)
        .options(
            selectinload(Project.organization),
            selectinload(Project.members).selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(Project.members).selectinload(ProjectMember.role)
        )
        .where(Project.organization_id == organization_id)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_projects_by_member(db: AsyncSession, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Project]:
    """Fetch projects assigned to a specific user.

    Args:
        db: Database session.
        user_id: User identifier.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        List[Project]: Projects assigned to the user.
    """
    stmt = (
        select(Project)
        .join(Project.members)
        .options(
            selectinload(Project.organization),
            selectinload(Project.members).selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(Project.members).selectinload(ProjectMember.role)
        )
        .where(
            ProjectMember.user_id == user_id,
            ProjectMember.is_active == True,
            Project.is_active == True
        )
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_project_by_id_for_member(db: AsyncSession, project_id: UUID, user_id: UUID) -> Optional[Project]:
    """Fetch a project by ID when the user is assigned to it.

    Args:
        db: Database session.
        project_id: Project identifier.
        user_id: User identifier.

    Returns:
        Optional[Project]: Matching project, if the user has access.
    """
    stmt = (
        select(Project)
        .join(Project.members)
        .options(
            selectinload(Project.organization),
            selectinload(Project.members).selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(Project.members).selectinload(ProjectMember.role)
        )
        .where(
            Project.id == project_id,
            ProjectMember.user_id == user_id,
            ProjectMember.is_active == True,
            Project.is_active == True
        )
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_all_projects(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Project]:
    """Fetch all projects.

    Args:
        db: Database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        List[Project]: Project records.
    """
    stmt = (
        select(Project)
        .options(
            selectinload(Project.organization),
            selectinload(Project.members).selectinload(ProjectMember.user).selectinload(User.role),
            selectinload(Project.members).selectinload(ProjectMember.role)
        )
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def create_project(db: AsyncSession, project_data: dict) -> Project:
    """Create a project.

    Args:
        db: Database session.
        project_data: Project creation payload as a dict.

    Returns:
        Project: Newly created project.
    """

    project_obj = Project(**project_data)
    db.add(project_obj)
    await db.commit()
    await db.refresh(project_obj, attribute_names=["organization"])

    return project_obj


async def update_project(db: AsyncSession, project: Project, update_data: dict, updated_by_id: UUID) -> Project:
    """Update a project with audit tracking.

    Args:
        db: Database session.
        project: Project instance to update.
        update_data: Fields to update.
        updated_by_id: Identifier of the user updating the project.

    Returns:
        Project: Updated project.
    """
    for key, value in update_data.items():
        if hasattr(project, key):
            setattr(project, key, value)

    project.updated_by = updated_by_id
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


async def delete_project(db: AsyncSession, project: Project, deleted_by_id: UUID) -> Project:
    """Soft-delete a project with audit tracking.

    Args:
        db: Database session.
        project: Project instance to delete.
        deleted_by_id: Identifier of the user deleting the project.

    Returns:
        Project: Soft-deleted project.
    """
    project.is_active = False
    project.deleted_by = deleted_by_id
    project.deleted_at = datetime.now(timezone.utc)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project
