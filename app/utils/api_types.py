from pydantic import BaseModel
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class CreateRequest(BaseModel):
    text: str

class CreateResponse(BaseModel):
    text: str
    summary: str
    createdAt: str

# Database model for storing summaries
class Summary(Base):
    __tablename__ = "summaries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc)) # CHECK THIS 
