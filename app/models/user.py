# models/user.py
from sqlalchemy import Column, String, DateTime
from datetime import datetime
from app.db.database import Base
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid, unique=True, index=True)
    userID = Column(String, nullable=False)
    userName = Column(String, nullable=False)
    userType = Column(String, nullable=False)  # "doctor" or "patient"
    userEmail = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
