"""Authentication service layer."""

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.auth_repository import (
    create_password_reset_token,
    get_password_reset_token,
    mark_token_as_used,
    get_user_by_email,
)
from app.repositories.user_repository import update_user_password
from app.schemas.login_schemas import ForgotPasswordRequest, ResetPasswordRequest
from app.schemas.response_schemas import APIResponse
from app.utils.email_utils import send_password_reset_email


class AuthService:
    """Service for authentication operations."""

    def __init__(self, db: AsyncSession):
        """Initialize service with database session.

        Args:
            db: Database session.
        """
        self.db = db

    async def forgot_password_service(self, request: ForgotPasswordRequest) -> APIResponse:
        """Handle forgot password request.

        Args:
            request: Forgot password request data.

        Returns:
            APIResponse with success message.

        Raises:
            HTTPException: If user not found.
        """
        # Check if user exists
        user = await get_user_by_email(self.db, request.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Create reset token
        token = await create_password_reset_token(self.db, user.id)

        # Send email
        await send_password_reset_email(user.email, token)

        return APIResponse.success_response("Password reset email sent successfully")

    async def reset_password_service(self, request: ResetPasswordRequest) -> APIResponse:
        """Handle password reset request.

        Args:
            request: Reset password request data.

        Returns:
            APIResponse with success message.

        Raises:
            HTTPException: If token is invalid or expired.
        """
        # Get token
        reset_token = await get_password_reset_token(self.db, request.token)
        if not reset_token or not reset_token.is_valid():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired token"
            )

        # Update password
        await update_user_password(self.db, reset_token.user_id, request.new_password)

        # Mark token as used
        await mark_token_as_used(self.db, request.token)

        return APIResponse.success_response("Password reset successfully")