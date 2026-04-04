
from database import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

class Blog(Base):

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
    images = relationship("BlogImage", back_populates="blog", cascade="all, delete-orphan")


class BlogImage(Base):

    __tablename__ = "blog_images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    blog_id = Column(
        Integer,
        ForeignKey("blogs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    blog = relationship("Blog", back_populates="images")

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=True)

    blogs = relationship("Blog", back_populates="creator")
    comments = relationship("Comment", back_populates="creator")
    replies = relationship("Reply", back_populates="creator")
    likes = relationship("Like", back_populates="creator")
    my_fav = relationship("MyFav", back_populates="creator")
    user_profiles = relationship("UserProfile", back_populates="creator")
    password_reset_tokens = relationship("PasswordResetToken", back_populates="creator")

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


class PasswordResetToken(Base):

    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(32), unique=True, nullable=False, index=True)
    is_used = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    creator = relationship("User", back_populates="password_reset_tokens")
