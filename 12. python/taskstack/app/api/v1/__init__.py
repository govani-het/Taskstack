"""Version 1 API package."""

from fastapi import APIRouter

from .routes.users import router as users_router
from .routes.roles import router as roles_router
from .routes.subscriptions import router as subscriptions_router
from .routes.organizations import router as organizations_router
from .routes.organization_subscriptions import router as organization_subscriptions_router
from .routes.projects import router as projects_router
from .routes.project_members import router as project_members_router
from .routes.tickets import router as tickets_router
from .routes.comments import router as comments_router
from .routes.replies import router as replies_router
from .routes.work_logs import router as work_logs_router

router = APIRouter(prefix="/app/v1")
router.include_router(users_router)
router.include_router(roles_router)
router.include_router(subscriptions_router)
router.include_router(organizations_router)
router.include_router(organization_subscriptions_router)
router.include_router(projects_router)
router.include_router(project_members_router)
router.include_router(tickets_router)
router.include_router(comments_router)
router.include_router(replies_router)
router.include_router(work_logs_router)
