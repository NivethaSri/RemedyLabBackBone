from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from ..schemas.recommendation_schema import DoctorRecommendationRequest
from ..services.recommendation_service import save_doctor_recommendation
from ..services.recommendation_service import get_doctor_recommendation
from ..schemas.recommendation_schema import DoctorRecommendationResponse

from app.schemas.recommendation_schema import (
    GenerateRecommendationRequest,
    AIRecommendationResponse,
)
from app.services.recommendation_service import generate_ai_recommendation_service
from app.services.recommendation_service import save_doctor_recommendation

router = APIRouter()


@router.post("/generate-recommendation", response_model=AIRecommendationResponse)
def generate_ai_recommendation(
    request: GenerateRecommendationRequest, db: Session = Depends(get_db)
):
    report, error = generate_ai_recommendation_service(str(request.report_id), db)

    if error:
        raise HTTPException(status_code=404, detail=error)

    return AIRecommendationResponse(
        report_id=report.id, ai_recommendation=report.ai_recommendation
    )


@router.post("/save-recommendation")
def save_recommendation(
    payload: DoctorRecommendationRequest, db: Session = Depends(get_db)
):
    report, error = save_doctor_recommendation(
        payload.report_id, payload.doctor_recommendation, db
    )
    if error:
        raise HTTPException(status_code=404, detail=error)

    return {
        "message": "Doctor recommendation saved successfully",
        "report_id": report.id,
    }


@router.get(
    "/get-recommendation/{report_id}", response_model=DoctorRecommendationResponse
)
def fetch_doctor_recommendation(report_id: str, db: Session = Depends(get_db)):
    data, error = get_doctor_recommendation(report_id, db)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return data
