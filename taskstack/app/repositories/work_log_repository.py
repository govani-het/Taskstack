"""Work log repository."""

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status

from app.models.work_log import WorkLog
from app.models.project_member import ProjectMember
from app.models.ticket import Ticket
from app.models.projects import Project
from app.repositories.audit import mark_deleted
from app.constant.work_log_constant import (
    ERROR_WORK_LOG_NOT_FOUND,
    ERROR_WORK_LOG_ACCESS_DENIED,
    ERROR_TICKET_NOT_FOUND,
    ERROR_PROJECT_ACCESS_DENIED,
    ERROR_WORK_LOG_UPDATE_DENIED,
    ERROR_WORK_LOG_DELETE_DENIED,
)
from app.constant.role_constant import (
    ROLE_ADMIN,
    ROLE_PROJECT_MANAGER,
    ROLE_DEVELOPER,
    ROLE_REPORTER,
)


async def get_work_logs(
    db: AsyncSession,
    current_user: dict,
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[UUID] = None,
    ticket_id: Optional[UUID] = None,
) -> List[WorkLog]:
    """Get work logs based on user role and permissions."""
    query = select(WorkLog).where(WorkLog.is_active == True)

    if current_user["role"] == ROLE_ADMIN:
        query = query.join(Ticket, WorkLog.ticket_id == Ticket.id)\
                     .join(Project, Ticket.project_id == Project.id)\
                     .where(Project.organization_id == current_user["organization_id"])

    elif current_user["role"] == ROLE_PROJECT_MANAGER:
        query = query.join(ProjectMember,
                           and_(WorkLog.created_by == ProjectMember.id,
                                WorkLog.project_id == ProjectMember.project_id))\
                     .where(ProjectMember.project_manager_id == current_user["id"])

    elif current_user["role"] in [ROLE_DEVELOPER, ROLE_REPORTER]:
        member_query = select(ProjectMember.id).where(
            ProjectMember.user_id == current_user["id"],
            ProjectMember.is_active == True,
        )
        member_ids = (await db.execute(member_query)).scalars().all()
        if member_ids:
            query = query.where(WorkLog.created_by.in_(member_ids))
        else:
            return []

    if project_id:
        query = query.where(WorkLog.project_id == project_id)
    if ticket_id:
        query = query.where(WorkLog.ticket_id == ticket_id)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_work_log_by_id(db: AsyncSession, work_log_id: UUID, current_user: dict) -> WorkLog:
    """Get a specific work log by ID with access control."""
    query = select(WorkLog).where(
        and_(WorkLog.id == work_log_id, WorkLog.is_active == True)
    )

    if current_user["role"] == ROLE_ADMIN:
        query = query.join(Ticket, WorkLog.ticket_id == Ticket.id)\
                     .join(Project, Ticket.project_id == Project.id)\
                     .where(Project.organization_id == current_user["organization_id"])

    elif current_user["role"] == ROLE_PROJECT_MANAGER:
        query = query.join(ProjectMember,
                           and_(WorkLog.created_by == ProjectMember.id,
                                WorkLog.project_id == ProjectMember.project_id))\
                     .where(ProjectMember.project_manager_id == current_user["id"])

    elif current_user["role"] in [ROLE_DEVELOPER, ROLE_REPORTER]:
        member_query = select(ProjectMember.id).where(
            ProjectMember.user_id == current_user["id"],
            ProjectMember.is_active == True,
        )
        member_ids = (await db.execute(member_query)).scalars().all()
        if member_ids:
            query = query.where(WorkLog.created_by.in_(member_ids))
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ERROR_WORK_LOG_ACCESS_DENIED,
            )

    result = await db.execute(query)
    work_log = result.scalar_one_or_none()
    if not work_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_WORK_LOG_NOT_FOUND,
        )
    return work_log


async def create_work_log(db: AsyncSession, work_log_data: dict, current_user: dict) -> WorkLog:
    """Create a new work log with access control."""
    ticket_query = select(Ticket).where(
        and_(Ticket.id == work_log_data["ticket_id"], Ticket.is_active == True)
    )
    ticket_result = await db.execute(ticket_query)
    ticket = ticket_result.scalar_one_or_none()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_TICKET_NOT_FOUND,
        )

    member_query = select(ProjectMember).where(
        and_(ProjectMember.user_id == current_user["id"],
             ProjectMember.project_id == ticket.project_id,
             ProjectMember.is_active == True)
    )
    member_result = await db.execute(member_query)
    member = member_result.scalar_one_or_none()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_PROJECT_ACCESS_DENIED,
        )

    work_log = WorkLog(
        project_id=ticket.project_id,
        ticket_id=work_log_data["ticket_id"],
        description=work_log_data.get("description"),
        time_spent_minutes=work_log_data["time_spent_minutes"],
        created_by=member.id,
        updated_by=member.id,
    )

    db.add(work_log)
    await db.commit()
    await db.refresh(work_log)
    return work_log


async def update_work_log(
    db: AsyncSession,
    work_log_id: UUID,
    update_data: dict,
    current_user: dict,
) -> WorkLog:
    """Update a work log with access control."""
    work_log = await get_work_log_by_id(db, work_log_id, current_user)

    can_update = False

    if current_user["role"] == ROLE_ADMIN:
        org_query = select(Project.organization_id)\
                   .join(Ticket, Project.id == Ticket.project_id)\
                   .where(Ticket.id == work_log.ticket_id)
        org_result = await db.execute(org_query)
        org_id = org_result.scalar_one_or_none()
        can_update = org_id == current_user["organization_id"]

    elif current_user["role"] == ROLE_PROJECT_MANAGER:
        pm_query = select(ProjectMember.project_manager_id)\
                  .where(and_(ProjectMember.id == work_log.created_by,
                            ProjectMember.project_id == work_log.project_id))
        pm_result = await db.execute(pm_query)
        pm_id = pm_result.scalar_one_or_none()
        can_update = pm_id == current_user["id"]

    else:
        creator_query = select(ProjectMember.user_id)\
                       .where(and_(ProjectMember.id == work_log.created_by,
                                 ProjectMember.project_id == work_log.project_id))
        creator_result = await db.execute(creator_query)
        creator_id = creator_result.scalar_one_or_none()
        can_update = creator_id == current_user["id"]

    if not can_update:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_WORK_LOG_UPDATE_DENIED,
        )

    for field, value in update_data.items():
        if value is not None:
            setattr(work_log, field, value)

    member_query = select(ProjectMember.id).where(
        and_(ProjectMember.user_id == current_user["id"],
             ProjectMember.project_id == work_log.project_id)
    )
    member_result = await db.execute(member_query)
    member_id = member_result.scalar_one_or_none()
    if member_id:
        work_log.updated_by = member_id

    await db.commit()
    await db.refresh(work_log)
    return work_log


async def delete_work_log(db: AsyncSession, work_log_id: UUID, current_user: dict) -> bool:
    """Soft delete a work log with access control."""
    work_log = await get_work_log_by_id(db, work_log_id, current_user)

    can_delete = False

    if current_user["role"] == ROLE_ADMIN:
        org_query = select(Project.organization_id)\
                   .join(Ticket, Project.id == Ticket.project_id)\
                   .where(Ticket.id == work_log.ticket_id)
        org_result = await db.execute(org_query)
        org_id = org_result.scalar_one_or_none()
        can_delete = org_id == current_user["organization_id"]

    elif current_user["role"] == ROLE_PROJECT_MANAGER:
        pm_query = select(ProjectMember.project_manager_id)\
                  .where(and_(ProjectMember.id == work_log.created_by,
                            ProjectMember.project_id == work_log.project_id))
        pm_result = await db.execute(pm_query)
        pm_id = pm_result.scalar_one_or_none()
        can_delete = pm_id == current_user["id"]

    else:
        creator_query = select(ProjectMember.user_id)\
                       .where(and_(ProjectMember.id == work_log.created_by,
                                 ProjectMember.project_id == work_log.project_id))
        creator_result = await db.execute(creator_query)
        creator_id = creator_result.scalar_one_or_none()
        can_delete = creator_id == current_user["id"]

    if not can_delete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_WORK_LOG_DELETE_DENIED,
        )

    member_query = select(ProjectMember.id).where(
        and_(ProjectMember.user_id == current_user["id"],
             ProjectMember.project_id == work_log.project_id,
             ProjectMember.is_active == True)
    )
    member_result = await db.execute(member_query)
    member_id = member_result.scalar_one_or_none()
    mark_deleted(work_log, member_id)

    await db.commit()
    return True
