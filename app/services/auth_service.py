from ..models.doctor import Doctor
from ..models.patient import Patient
from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ✅ LOGIN FUNCTION
def login_doctor(email: str, password: str, db: Session):
    doctor = db.query(Doctor).filter(Doctor.email == email).first()

    if not doctor or not verify_password(password, doctor.password):
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "message": "Invalid doctor credentials",
                "error": {"code": 401, "details": "Email or password is incorrect"},
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    return {
        "status": "success",
        "message": "Login successful",
        "data": {
            "id": doctor.id,
            "name": doctor.name,
            "email": doctor.email,
            "role": "doctor",
            "specialization": doctor.specialization,
            "experience": doctor.experience,
            "contactNumber": doctor.contact_number,
            "gender": doctor.gender,
            "age": ""  # Doctor has no age
        },
        "timestamp": datetime.utcnow().isoformat()
    }

# ✅ PATIENT LOGIN
def login_patient(email: str, password: str, db: Session):
    patient = db.query(Patient).filter(Patient.email == email).first()

    if not patient or not verify_password(password, patient.password):
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "message": "Invalid patient credentials",
                "error": {"code": 401, "details": "Email or password is incorrect"},
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    return {
        "status": "success",
        "message": "Login successful",
        "data": {
            "id": patient.id,
            "name": patient.name,
            "email": patient.email,
            "role": "patient",
            "specialization": None,
            "experience": None,
            "contactNumber": patient.contact_number,
            "gender": patient.gender,
            "age": patient.age or ""
        },
        "timestamp": datetime.utcnow().isoformat()
    }

# ✅ REGISTER DOCTOR
def register_doctor(data, db: Session):
    # Check if email already exists
    if db.query(Doctor).filter(Doctor.email == data.email).first() or db.query(Patient).filter(Patient.email == data.email).first():
        raise HTTPException(
            status_code=409,
            detail={
                "status": "error",
                "message": "Email already exists",
                "error": {"code": 409, "details": f"The email {data.email} is already registered"},
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    new_doctor = Doctor(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        specialization=data.specialization,
        contact_number=data.contactNumber,
        experience=str(data.experience),
        gender=data.gender,
        created_at=datetime.utcnow()
    )
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return {
        "status": "success",
        "message": "Doctor registered successfully",
        "data": {
            "id": new_doctor.id,
            "name": new_doctor.name,
            "email": new_doctor.email,
            "role": "doctor",
            "specialization": new_doctor.specialization,
            "experience": new_doctor.experience,
            "contactNumber": new_doctor.contact_number,
            "gender": new_doctor.gender,
            "age": "",
            "created_at": new_doctor.created_at.isoformat()
        },
        "timestamp": datetime.utcnow().isoformat()
    }

# ✅ REGISTER PATIENT
def register_patient(data, db: Session):
    # Check if email already exists
    if db.query(Patient).filter(Patient.email == data.email).first() or db.query(Doctor).filter(Doctor.email == data.email).first():
        raise HTTPException(
            status_code=409,
            detail={
                "status": "error",
                "message": "Email already exists",
                "error": {"code": 409, "details": f"The email {data.email} is already registered"},
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    new_patient = Patient(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        age=str(data.age),
        gender=data.gender,
        contact_number=data.contactNumber,
        created_at=datetime.utcnow()
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return {
        "status": "success",
        "message": "Patient registered successfully",
        "data": {
            "id": new_patient.id,
            "name": new_patient.name,
            "email": new_patient.email,
            "role": "patient",
            "age": new_patient.age,
            "gender": new_patient.gender,
            "contactNumber": new_patient.contact_number,
            "specialization": None,
            "experience": None,
            "created_at": new_patient.created_at.isoformat()
        },
        "timestamp": datetime.utcnow().isoformat()
    }
