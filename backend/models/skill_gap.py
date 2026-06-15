from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class SkillGap(Base):
    __tablename__ = "skill_gaps"

    gap_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    skills = Column(JSON, default=list)  # List of objects: [{"skill": "FastAPI", "status": "Missing", "priority": "High"}]
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="skill_gaps")
