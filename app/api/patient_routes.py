from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.health_report import Report
from app.schemas.patient_schema import PatientReportResponse
from uuid import UUID

router = APIRouter()

@router.get("/reports/{patient_id}", response_model=list[PatientReportResponse])
def get_reports_for_patient(patient_id: UUID, db: Session = Depends(get_db)):
    reports = db.query(Report).filter(Report.patient_id == str(patient_id)).all()
    return reports
