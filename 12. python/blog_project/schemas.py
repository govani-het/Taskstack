"""
    Defines the schemas module.
    
    Parameters:
    None (None): This module does not accept parameters.
    
    Returns:
    None: This module does not return a value.
"""

from datetime import datetime,date
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


def _validate_dob_age_range(value: date):
    """
        Handles the validate dob age range operation.
        
        Parameters:
        value (date): The value value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

    if age < 1 or age > 150:
        raise ValueError("User age must be between 1 and 150 years")

    return value

def validate_name(value:str):
    """
        Handles the validate name operation.
        
        Parameters:
        value (str): The value value used by this function.
        
        Returns:
        Any: The result produced by this function.
    """
    value = value.strip()
    if not value:
        raise ValueError("Name cannot be empty")

    if not all(char.isalpha() or char in {" ", "-", "'"} for char in value):
        raise ValueError("Name can contain only letters, spaces, hyphen, and apostrophe")

    return value


#this is blog schemas
class BlogCreate(BaseModel):
    """
        Represents the BlogCreate class.
        
        Parameters:
        None (None): This class definition does not accept runtime parameters.
        
        Returns:
        None: This class definition does not return a value.
    """
    title: str
    body: str

    class Config:
        from_attributes = True

class BlogUpdate(BaseModel):
    """
        Represents the BlogUpdate class.
        
        Parameters:
        None (None): This class definition does not accept runtime parameters.
        
        Returns:
        None: This class definition does not return a value.
    """

    title: Optional[str] = None
    body: Optional[str] = None


#this is user schemas

class SimpleUser(BaseModel):

    name: str
    email: EmailStr
    class Config:
        from_attributes = True

class ShowUser(BaseModel):
    """
        Represents the ShowUser class.
        
        Parameters:
        None (None): This class definition does not accept runtime parameters.
        
        Returns:
        None: This class definition does not return a value.
    """

    name: str
    email: EmailStr
    blogs: List[BlogCreate] = Field(default_factory=list)

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    """
        Represents the UserCreate class.
        
        Parameters:
        None (None): This class definition does not accept runtime parameters.
        
        Returns:
        None: This class definition does not return a value.
    """

    name: str
    email: EmailStr
    password: str

    @field_validator("name")
    @classmethod
    def validate_user_name(cls, value: str) -> str:
        """
            Handles the validate user name operation.
            
            Parameters:
            value (str): The value value used by this function.
            
            Returns:
            str: The result produced by this function.
        """
        return validate_name(value)

class User(BaseModel):
    """
        Represents the User class.
        
        Parameters:
        None (None): This class definition does not accept runtime parameters.
        
        Returns:
        None: This class definition does not return a value.
    """

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
        """
            Handles the validate first name operation.
            
            Parameters:
            value (str): The value value used by this function.
            
            Returns:
            str: The result produced by this function.
        """
        return validate_name(value)

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, value: str) -> str:
        """
            Handles the validate last name operation.
            
            Parameters:
            value (str): The value value used by this function.
            
            Returns:
            str: The result produced by this function.
        """
        return validate_name(value)

    @field_validator("dob")
    @classmethod
    def validate_dob(cls, value: date) -> date:
        """
            Handles the validate dob operation.
            
            Parameters:
            value (date): The value value used by this function.
            
            Returns:
            date: The result produced by this function.
        """
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
        """
            Handles the validate first name operation.
            
            Parameters:
            value (Optional str): The value value used by this function.
            
            Returns:
            Optional str: The result produced by this function.
        """
        if value is None:
            return value
        return validate_name(value)

    @field_validator("last_name")
    @classmethod
    def validate_last_name(cls, value: Optional[str]) -> Optional[str]:
        """
            Handles the validate last name operation.
            
            Parameters:
            value (Optional str): The value value used by this function.
            
            Returns:
            Optional str: The result produced by this function.
        """
        if value is None:
            return value
        return validate_name(value)

    @field_validator("dob")
    @classmethod
    def validate_dob(cls, value: Optional[date]) -> Optional[date]:
        """
            Handles the validate dob operation.
            
            Parameters:
            value (Optional date): The value value used by this function.
            
            Returns:
            Optional date: The result produced by this function.
        """
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
    """
        Represents the ShowBlog class.
        
        Parameters:
        None (None): This class definition does not accept runtime parameters.
        
        Returns:
        None: This class definition does not return a value.
    """

    title: str
    body: str
    created_at: Optional[datetime] = None
    creator: Username
    comments: List[Comment] = None
    

    class Config:
        from_attributes = True
