"""Pydantic schemas used for request validation and response serialization."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

#this is blog schemas

class BlogBase(BaseModel):
    """Shared fields for blog payloads."""
    title: str
    body: str


class BlogCreate(BlogBase):
    """Schema for returning a stored blog record."""

    id: int
    user_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BlogUpdate(BaseModel):
    """Schema for partial updates on blog fields."""

    title: Optional[str] = None
    body: Optional[str] = None
    user_id: Optional[int] = None

#this is user schemas

class SimpleUser(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class ShowUser(BaseModel):
    """Schema used when returning user details with nested blogs."""

    name: str
    email: EmailStr
    blogs: List[BlogCreate] = Field(default_factory=list)

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    """Schema for creating a user."""

    name: str
    email: EmailStr
    password: str

class User(BaseModel):
    """Schema for returning a stored user."""

    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class Username(BaseModel):
    name:str

#this is auth schemas
class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


#this is reply schemas
class ReplyCreate(BaseModel):
    content: str
    user_id: int


class ShowReply(BaseModel):
    creator:Username
    content:str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


#this is Comment Schemas
class CommentCreate(BaseModel):
    content: str
    user_id: int


class Comment(BaseModel):
    creator:Username
    content:str
    created_at: Optional[datetime] = None
    replies: List[ShowReply] = None

    class Config:
        from_attributes = True



class ShowBlog(BaseModel):
    """Schema used when returning a blog with its creator information."""

    title: str
    body: str
    created_at: Optional[datetime] = None
    creator: SimpleUser
    comments: List[Comment] = None
    

    class Config:
        from_attributes = True
