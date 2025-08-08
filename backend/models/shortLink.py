from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

from backend.databases.postgres import Base

class ShortLink(Base):
    __tablename__ = "ShortLinks"

    id_link = Column(Integer, primary_key=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    is_protected = Column(Boolean, default=False)
    password = Column(String, nullable=True)
    custom_domain = Column(String, nullable=True)

    id_creator = Column(Integer, ForeignKey("Users.id_user"), nullable=False)
    id_tag = Column(Integer, ForeignKey("Tags.id_tag"), nullable=True)

    creator = relationship("User", back_populates="links")
    tag = relationship("Tag", back_populates="links")

    clicks = relationship("LinkClick", back_populates="link")

class Tag(Base):
    __tablename__ = "Tags"

    id_tag = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    links = relationship("ShortLink", back_populates="tag")