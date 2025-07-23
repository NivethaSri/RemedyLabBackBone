from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
from app.db.database import Base


def generate_uuid():
    return str(uuid.uuid4())




class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, default=generate_uuid, unique=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    contact_number = Column(String, nullable=True)  # Renamed from phone_number
    age = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
