from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.config.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    users = relationship("User", back_populates="role")
