from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..schemas.doctor_schema import DoctorSignup
from ..schemas.patient_schema import PatientSignup
from ..schemas.auth_schema import LoginRequest, LoginResponse

from ..services.auth_service import register_doctor, register_patient, login_doctor, login_patient

router = APIRouter()

@router.post("/doctor/signup")
def signup_doctor(data: DoctorSignup, db: Session = Depends(get_db)):
    return register_doctor(data, db)

@router.post("/patient/signup")
def signup_patient(data: PatientSignup, db: Session = Depends(get_db)):
    return register_patient(data, db)

@router.post("/doctor/login")
def doctor_login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_doctor(request.email, request.password, db)

@router.post("/patient/login")
def patient_login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_patient(request.email, request.password, db)
