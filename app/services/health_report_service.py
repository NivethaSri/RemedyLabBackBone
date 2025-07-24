import os
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import UploadFile , HTTPException
from app.models.health_report import Report
from app.services.extractor_service import extract_text  # your existing function
from uuid import UUID

UPLOAD_DIR = "uploaded_reports"

def save_report(file: UploadFile, patient_id: uuid.UUID, doctor_id: uuid.UUID, db: Session):
    # Ensure the upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Generate a unique filename
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    full_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Save the uploaded file
    with open(full_path, "wb") as f:
        f.write(file.file.read())

    # 🔍 Extract metrics from the saved PDF
    parsed = extract_text(full_path)

    print("parsed", parsed)
    # 📝 Create a new Report record
    new_report = Report(
        id=uuid.uuid4(),
        file_name=file.filename,
        file_path=full_path,
        uploaded_at=datetime.utcnow(),
        patient_id=patient_id,
        doctor_id=doctor_id,
        metrics=parsed  # <-- Store the extracted metrics JSON
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return new_report


def update_recommendation(report_id: UUID, recommendation: str, db: Session):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    report.ai_recommendation = recommendation
    db.commit()
    db.refresh(report)
    return {"message": "Recommendation updated successfully"}

def add_doctor_recommendation(report_id: UUID, recommendation: str, db: Session):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise ValueError("Report not found")

    report.doctor_recommendation = recommendation
    db.commit()
    db.refresh(report)
    return {"message": "Doctor recommendation saved successfully"}
