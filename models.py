from sqlalchemy import Column, Integer, String
from database import Base

class Submission(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    discord_id = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    mobile_no = Column(String)
    country = Column(String)
