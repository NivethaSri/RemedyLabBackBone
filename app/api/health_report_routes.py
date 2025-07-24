from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException,Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.health_report_service import save_report
from uuid import UUID
from app.schemas.health_report_schema import RecommendationRequest
from app.models.health_report import Report
from app.schemas.health_report_schema import DoctorRecommendationRequest
from app.services.health_report_service import add_doctor_recommendation
import os
from fastapi.responses import FileResponse


router = APIRouter()

@router.post("/upload-report")
def upload_report(
    file: UploadFile = File(...),
    patient_id: UUID = Form(...),
    doctor_id: UUID = Form(...),
    db: Session = Depends(get_db)
):
    return save_report(file, patient_id, doctor_id, db)

@router.post("/add-ai_recommendation")
def add_ai_recommendation(data: RecommendationRequest, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == data.report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    report.ai_recommendation = data.ai_recommendation
    db.commit()
    return {"message": "AI_Recommendation saved successfully"}

@router.post("/add-doctor-recommendation")
def add_doctor_recommendation_api(payload: DoctorRecommendationRequest, db: Session = Depends(get_db)):
    try:
        return add_doctor_recommendation(payload.report_id, payload.doctor_recommendation, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/download_report")
def download_report(file_path: str = Query(..., description="Relative path to the report file")):
    abs_path = os.path.join(os.getcwd(), file_path)

    if not os.path.isfile(abs_path):
        raise HTTPException(status_code=404, detail="File not found")

    filename = os.path.basename(abs_path)
    return FileResponse(abs_path, filename=filename, media_type='application/octet-stream')
