from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class ReadinessScore(Base):
    __tablename__ = "readiness_scores"

    score_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    resume_weight_score = Column(Float, default=0.0)
    coding_weight_score = Column(Float, default=0.0)
    technical_weight_score = Column(Float, default=0.0)
    hr_weight_score = Column(Float, default=0.0)
    project_weight_score = Column(Float, default=0.0)
    overall_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="readiness_scores")
