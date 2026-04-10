import uuid

from sqlalchemy import UUID, Column, String, Text
from sqlalchemy.orm import relationship

from app.config.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    users = relationship("User", back_populates="role")
    project_members = relationship("ProjectMember", back_populates="role")
