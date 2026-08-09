from sqlalchemy import Column , Integer , String , Text ,DateTime , JSON, ForeignKey
from sqlalchemy.sql import func
from .db import Base

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer , primary_key = True)
    name = Column(String , unique = True , nullable=False)
    career_url = Column(String ,nullable= False)
    ats_type =Column(String , nullable = True)

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer , primary_key = True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    title = Column(String)
    location = Column(String)
    url = Column(String, unique=True)
    posted_date = Column(String)
    raw = Column(JSON)
    normalized_role = Column(String)
    match_score = Column(Integer, default=0)
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())