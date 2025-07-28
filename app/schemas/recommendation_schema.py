from pydantic import BaseModel
from uuid import UUID


class GenerateRecommendationRequest(BaseModel):
    report_id: UUID


class AIRecommendationResponse(BaseModel):
    report_id: UUID
    ai_recommendation: str


class DoctorRecommendationRequest(BaseModel):
    report_id: str
    doctor_recommendation: str


class DoctorRecommendationResponse(BaseModel):
    report_id: str
    doctor_recommendation: str | None
    patient_id: str
