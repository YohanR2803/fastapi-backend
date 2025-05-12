# models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base
from datetime import datetime

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    discord_id = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    mobile_no = Column(String)
    country = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    verified = Column(Boolean, default=False)
