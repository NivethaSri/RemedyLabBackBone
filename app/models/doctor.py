from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
from app.db.database import Base
from sqlalchemy.orm import relationship


def generate_uuid():
    return str(uuid.uuid4())



class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(String, primary_key=True, default=generate_uuid, unique=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    specialization = Column(String)
    contact_number = Column(String)
    experience = Column(String)
    gender = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    reports = relationship("Report", back_populates="doctor")
