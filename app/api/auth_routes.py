from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..schemas.doctor_schema import DoctorSignup
from ..schemas.patient_schema import PatientSignup
from ..schemas.auth_schema import LoginRequest, LoginResponse

from ..services.auth_service import register_doctor, register_patient, login_user

router = APIRouter()

@router.post("/signup/doctor")
def signup_doctor(data: DoctorSignup, db: Session = Depends(get_db)):
    return register_doctor(data, db)

@router.post("/signup/patient")
def signup_patient(data: PatientSignup, db: Session = Depends(get_db)):
    return register_patient(data, db)


@router.post("/signin", response_model=LoginResponse)
def signin(data: LoginRequest, db: Session = Depends(get_db)):
    return login_user(data.email, data.password, db)