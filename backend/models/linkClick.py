from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.databases.postgres import Base

class LinkClick(Base):
    __tablename__ = "LinkClicks"

    id_click = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String, nullable=False)
    user_agent = Column(String, nullable=False)
    referer = Column(String, nullable=True)

    id_link = Column(Integer, ForeignKey("ShortLinks.id_link"))
    link = relationship("ShortLink", back_populates="clicks")