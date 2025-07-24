from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional, Dict, Any
from datetime import datetime
class ReportUploadRequest(BaseModel):
    patient_id: UUID
    doctor_id: UUID

class PatientInfo(BaseModel):
    id: UUID
    name: str
    email: str

    class Config:
        from_attributes = True

class ReportResponse(BaseModel):
    id: UUID
    file_name: str
    file_path: str
    uploaded_at: datetime
    patient: PatientInfo
    metrics: Optional[List[Dict[str, Any]]] = None  # <-- Include metrics here

    class Config:
        from_attributes = True


class RecommendationRequest(BaseModel):
    report_id: UUID
    ai_recommendation: str


class DoctorRecommendationRequest(BaseModel):
    report_id: UUID
    doctor_recommendation: str
