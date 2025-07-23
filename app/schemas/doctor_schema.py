from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID

class DoctorSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    specialization: str
    contact_number: str
    experience: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DoctorInfo(BaseModel):
    id: UUID
    name: str
    specialization: str | None = None
    experience: str | None = None

    class Config:
        from_attributes = True