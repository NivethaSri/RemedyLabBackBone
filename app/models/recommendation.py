from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    report_id = Column(UUID(as_uuid=True), ForeignKey("reports.id"), primary_key=True)
    ai_recommendation = Column(Text, nullable=True)
    doctor_recommendation = Column(Text, nullable=True)
