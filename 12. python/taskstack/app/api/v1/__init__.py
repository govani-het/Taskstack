from fastapi import APIRouter

from .routes.users import router as users_router

router = APIRouter(prefix="/app/v1")
router.include_router(users_router)