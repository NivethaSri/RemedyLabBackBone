from sqlalchemy.orm import Session
from app.models.doctor import Doctor

def get_all_doctors(db: Session):
    return db.query(Doctor).all()
