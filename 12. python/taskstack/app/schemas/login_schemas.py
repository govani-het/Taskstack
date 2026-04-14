from pydantic import BaseModel
from typing import Optional, List
from fastapi.security import OAuth2PasswordBearer



class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    username: str | None = None
    user_id: str | None = None
    role: str | None = None
    organization_id: str | None = None