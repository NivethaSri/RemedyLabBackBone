from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from ..schemas.doctor_schema import DoctorInfo
from ..services.doctor_service import get_all_doctors
from ..schemas.health_report_schema import ReportResponse
from ..models.health_report import Report
from uuid import UUID

router = APIRouter()

@router.get("/list", response_model=list[DoctorInfo])
def list_doctors(db: Session = Depends(get_db)):
    return get_all_doctors(db)

# New endpoint for fetching doctor-specific reports
@router.get("/reports/{doctor_id}", response_model=list[ReportResponse])
def get_reports_for_doctor(doctor_id: UUID, db: Session = Depends(get_db)):
    reports = db.query(Report).filter(Report.doctor_id == str(doctor_id)).all()

    if not reports:
        raise HTTPException(status_code=404, detail="No reports found for this doctor")

    return reports