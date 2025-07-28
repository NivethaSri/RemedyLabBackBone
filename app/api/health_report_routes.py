from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query
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
    db: Session = Depends(get_db),
):
    return save_report(file, patient_id, doctor_id, db)


@router.get("/download_report")
def download_report(
    file_path: str = Query(..., description="Relative path to the report file")
):
    abs_path = os.path.join(os.getcwd(), file_path)

    if not os.path.isfile(abs_path):
        raise HTTPException(status_code=404, detail="File not found")

    filename = os.path.basename(abs_path)
    return FileResponse(
        abs_path, filename=filename, media_type="application/octet-stream"
    )
