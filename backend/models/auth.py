from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from backend.databases.postgres import Base


class User(Base):
    __tablename__ = "Users"

    id_user = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    id_role = Column(Integer, ForeignKey("Roles.id_role"))
    created_at = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role", back_populates="user")

class Role(Base):
    __tablename__ = "Roles"

    id_role = Column(Integer, primary_key=True)
    role = Column(String, unique=True)

    user = relationship("User", back_populates="role")