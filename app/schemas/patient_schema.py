from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class PatientSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    age: int
    gender: str
    contact_number: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
