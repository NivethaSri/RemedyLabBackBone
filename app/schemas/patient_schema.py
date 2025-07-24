from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

from uuid import UUID


class PatientSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    age: int
    gender: str
    contact_number: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DoctorInfoBrief(BaseModel):
    id: UUID
    name: str
    email: str | None = None

    class Config:
        from_attributes = True

class PatientReportResponse(BaseModel):
    id: UUID
    file_name: str
    file_path: str
    uploaded_at: datetime
    ai_recommendation: str | None = None
    doctor: DoctorInfoBrief

    class Config:
        from_attributes = True