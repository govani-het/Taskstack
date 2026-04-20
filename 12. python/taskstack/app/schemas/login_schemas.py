"""Authentication schema definitions."""

from pydantic import BaseModel
from typing import Optional, List
from fastapi.security import OAuth2PasswordBearer



class Login(BaseModel):
    """Schema for login requests."""
    username: str
    password: str


class Token(BaseModel):
    """Schema for authentication tokens."""
    access_token: str
    token_type: str
    refresh_token: str


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token requests."""
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    """Schema for forgot password requests."""
    email: str


class ResetPasswordRequest(BaseModel):
    """Schema for reset password requests."""
    token: str
    new_password: str
