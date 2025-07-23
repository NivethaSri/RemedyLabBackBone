from ..models.doctor import Doctor
from ..models.patient import Patient
from ..db.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def login_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.userEmail == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {
        "userID": user.userID,
        "userType": user.userType,
        "email": user.userEmail,
        "message": "Login successful"
    }

def register_doctor(data, db: Session):
    
    if db.query(User).filter(User.userEmail == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    

    new_doctor = Doctor(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        specialization=data.specialization,
        contact_number=getattr(data, "contact_number", None),
        experience=getattr(data, "experience", ""),
        created_at=datetime.utcnow()
    )
    db.add(new_doctor)
    db.flush()  # get the ID before commit

    # Insert into users table
    new_user = User(
        userID=new_doctor.id,
        userType="doctor",
        userEmail=new_doctor.email,
        password=new_doctor.password,
        created_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor

def register_patient(data, db: Session):
    if db.query(User).filter(User.userEmail == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_patient = Patient(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        age=getattr(data, "age", None),
        gender=getattr(data, "gender", None),
        contact_number=getattr(data, "contact_number", None),
        created_at=datetime.utcnow()
    )
    db.add(new_patient)
    db.flush()  # get the ID before commit

    # Insert into users table
    new_user = User(
        userID=new_patient.id,
        userType="patient",
        userEmail=new_patient.email,
        password=new_patient.password,
        created_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_patient)
    return new_patient
