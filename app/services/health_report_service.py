import os
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from app.models.health_report import Report
from app.services.extractor_service import extract_text  # your existing function
from uuid import UUID

UPLOAD_DIR = "uploaded_reports"


def save_report(
    file: UploadFile, patient_id: uuid.UUID, doctor_id: uuid.UUID, db: Session
):
    try:
        # Ensure the upload directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Generate a unique filename
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        full_path = os.path.join(UPLOAD_DIR, unique_filename)

        # Save the uploaded file
        with open(full_path, "wb") as f:
            f.write(file.file.read())

        # 🔍 Extract metrics from the saved PDF
        parsed_metrics = extract_text(full_path)

        # 📝 Create a new Report record
        new_report = Report(
            id=uuid.uuid4(),
            file_name=file.filename,
            file_path=full_path,
            uploaded_at=datetime.utcnow(),
            patient_id=patient_id,
            doctor_id=doctor_id,
            metrics=parsed_metrics,  # Store extracted metrics JSON
        )
        db.add(new_report)
        db.commit()
        db.refresh(new_report)

        # ✅ Success Response
        response = {
            "status": "success",
            "message": "Report uploaded successfully",
            "data": {
                "report_id": str(new_report.id),
                "file_name": new_report.file_name,
                "file_path": new_report.file_path,
                "uploaded_at": new_report.uploaded_at.isoformat(),
                "patient_id": str(new_report.patient_id),
                "doctor_id": str(new_report.doctor_id),
                "metrics": new_report.metrics,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }

        return response

    except Exception as e:
        # ❌ Error Response
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "Failed to upload report",
                "error": {"code": 500, "details": str(e)},
                "timestamp": datetime.utcnow().isoformat(),
            },
        )


def update_recommendation(report_id: UUID, recommendation: str, db: Session):
    # Check if report exists
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": "Report not found",
                "error": {
                    "code": 404,
                    "details": f"No report found with ID {report_id}",
                },
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    # Update recommendation
    report.ai_recommendation = recommendation
    db.commit()
    db.refresh(report)

    # ✅ Success Response
    response = {
        "status": "success",
        "message": "Recommendation updated successfully",
        "data": {
            "report_id": str(report.id),
            "file_name": report.file_name,
            "ai_recommendation": report.ai_recommendation,
            "updated_at": datetime.utcnow().isoformat(),
        },
        "timestamp": datetime.utcnow().isoformat(),
    }

    return response


def add_doctor_recommendation(report_id: UUID, recommendation: str, db: Session):
    # Check if report exists
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": "Report not found",
                "error": {
                    "code": 404,
                    "details": f"No report found with ID {report_id}",
                },
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    # Update doctor recommendation
    report.doctor_recommendation = recommendation
    db.commit()
    db.refresh(report)

    # ✅ Success Response
    response = {
        "status": "success",
        "message": "Doctor recommendation saved successfully",
        "data": {
            "report_id": str(report.id),
            "file_name": report.file_name,
            "doctor_recommendation": report.doctor_recommendation,
            "updated_at": datetime.utcnow().isoformat(),
        },
        "timestamp": datetime.utcnow().isoformat(),
    }

    return response
