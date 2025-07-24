from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.database import Base
from sqlalchemy.dialects.postgresql import JSONB  # or JSON
from sqlalchemy import Text

class Report(Base):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(String, ForeignKey("doctors.id"), nullable=False)
    ai_recommendation = Column(Text, nullable=True)  # Supports large, multiline Markdown
    doctor_recommendation = Column(Text)  # <-- NEW COLUMN

    patient = relationship("Patient")
    doctor = relationship("Doctor", back_populates="reports")
    metrics = Column(JSONB)  # <- to store exact metrics JSON
