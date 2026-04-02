"""Pydantic schemas used for request validation and response serialization."""

from datetime import datetime,date
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


def _validate_dob_age_range(value: date):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

    if age < 1 or age > 150:
        raise ValueError("User age must be between 1 and 150 years")

    return value

def validate_name(value:str):
    value = value.strip()
    if not value:
        raise ValueError("Name cannot be empty")

    if not all(char.isalpha() or char in {" ", "-", "'"} for char in value):
        raise ValueError("Name can contain only letters, spaces, hyphen, and apostrophe")

    return value


#this is blog schemas
class BlogCreate(BaseModel):
    """Schema for returning a stored blog record."""
    title: str
    body: str

    class Config:
        from_attributes = True

class BlogUpdate(BaseModel):
    """Schema for partial updates on blog fields."""

    title: Optional[str] = None
    body: Optional[str] = None


#this is user schemas

class SimpleUser(BaseModel):

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

    @field_validator("name")
    @classmethod
    def validate_user_name(cls, value: str) -> str:
        return validate_name(value)

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
    user_id: int | None = None


#this is reply schemas
class ReplyCreate(BaseModel):
    content: str


class ShowReply(BaseModel):
    creator:Username
    content:str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


#this is Comment Schemas
class CommentCreate(BaseModel):
    content: str


class Comment(BaseModel):
    creator:Username
    content:str
    created_at: Optional[datetime] = None
    replies: List[ShowReply] = None

    class Config:
        from_attributes = True

#this is user profile schemas

class UserProfile(BaseModel):
    first_name:str
    last_name: str
    dob: date
    creator: SimpleUser

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, value: str) -> str:
        return validate_name(value)

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, value: str) -> str:
        return validate_name(value)

    @field_validator("dob")
    @classmethod
    def validate_dob(cls, value: date) -> date:
        return _validate_dob_age_range(value)

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[date] = None

    @field_validator("first_name")
    @classmethod
    def validate_first_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return validate_name(value)

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return validate_name(value)

    @field_validator("dob")
    @classmethod
    def validate_dob(cls, value: Optional[date]) -> Optional[date]:
        if value is None:
            return value

        return _validate_dob_age_range(value)

class ShowMyBlog(BaseModel):
    title: str
    body: str
    created_at: Optional[datetime] = None
    total_like_count: int
    comments: List[Comment] = []
    class Config:
        from_attributes = True

class FavBlog(BaseModel):
    title: str
    body: str
    created_at: Optional[datetime] = None
    creator: SimpleUser

    class Config:
        from_attributes = True

class ShowMyFavBlog(BaseModel):

    blog: FavBlog

    class Config:
        from_attributes = True

#----------------------------

class ShowBlog(BaseModel):
    """Schema used when returning a blog with its creator information."""

    title: str
    body: str
    created_at: Optional[datetime] = None
    creator: Username
    comments: List[Comment] = None
    

    class Config:
        from_attributes = True
