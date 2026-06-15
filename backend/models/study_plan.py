from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class StudyPlan(Base):
    __tablename__ = "study_plans"

    plan_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    tasks = Column(JSON, default=dict)  # {"Week 1": [{"task": "Arrays", "completed": false}], ...}
    completion_percentage = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="study_plans")
