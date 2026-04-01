"""Pydantic schemas used for request validation and response serialization."""

from pydantic import BaseModel,EmailStr
from typing import Optional, List





class Blog(BaseModel):
    """Schema for creating or representing a blog record."""

    id: int
    title: str
    body: str
    user_id: int

    class Config:
        from_attributes = True

class ShowUser(BaseModel):
    """Schema used when returning user details with nested blogs."""

    name: str
    email: EmailStr
    blogs : List[Blog] = []

    class Config:
        from_attributes = True

class User(BaseModel):
    """Schema for creating or representing a user."""

    id: int
    name: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class BlogUpdate(BaseModel):
    """Schema for partial updates on blog fields."""

    title: Optional[str] = None
    body: Optional[str] = None
    user_id: Optional[int] = None

class ShowBlog(BaseModel):
    """Schema used when returning a blog with its creator information."""

    title: str
    body: str
    creator: ShowUser

    class Config:
        from_attributes = True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
