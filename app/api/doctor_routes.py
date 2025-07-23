from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from ..schemas.doctor_schema import DoctorInfo
from ..services.doctor_service import get_all_doctors

router = APIRouter()

@router.get("/list", response_model=list[DoctorInfo])
def list_doctors(db: Session = Depends(get_db)):
    return get_all_doctors(db)
