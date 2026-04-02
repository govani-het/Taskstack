"""SQLAlchemy ORM models for blogs and users."""

from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

class Blog(Base):
    """Database model representing a blog post."""

    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="blogs")
    comments = relationship("Comment", back_populates="blog")
    likes = relationship("Like", back_populates="blog")
    my_fav = relationship("MyFav", back_populates="blog")

class User(Base):
    """Database model representing an application user."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship("Blog", back_populates="creator")
    comments = relationship("Comment", back_populates="creator")
    replies = relationship("Reply", back_populates="creator")
    likes = relationship("Like", back_populates="creator")
    my_fav = relationship("MyFav", back_populates="creator")
    user_profiles = relationship("UserProfile", back_populates="creator")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    blog_id = Column(Integer, ForeignKey("blogs.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="comments")
    blog = relationship("Blog", back_populates="comments")
    replies = relationship("Reply", back_populates="comments")

class Reply(Base):
    __tablename__ = "replies"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    comment_id = Column(Integer, ForeignKey("comments.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="replies")
    comments = relationship("Comment", back_populates="replies")

class Like(Base):
    __tablename__ = "like"

    id = Column(Integer, primary_key=True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"))
    blog_id = Column(Integer, ForeignKey("blogs.id"))

    creator = relationship("User",back_populates="likes")
    blog = relationship("Blog", back_populates="likes")

class MyFav(Base):

    __tablename__ = "my_favs"

    id = Column(Integer, primary_key=True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    blog_id = Column(Integer, ForeignKey("blogs.id"), nullable=False)

    creator = relationship("User",back_populates="my_fav")
    blog = relationship("Blog", back_populates="my_fav")

class UserProfile(Base):

    __tablename__ = "user_profile"

    id = Column(Integer, primary_key=True, index = True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    dob = Column(DateTime(timezone=True), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    creator = relationship("User", back_populates="user_profiles")