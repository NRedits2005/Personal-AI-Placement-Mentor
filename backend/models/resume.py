from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    resume_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    resume_path = Column(String(255), nullable=False)
    resume_score = Column(Integer, default=0)
    ats_score = Column(Integer, default=0)
    extracted_skills = Column(JSON, default=list)  # Stored as list of strings
    github_url = Column(String(255), nullable=True)
    linkedin_url = Column(String(255), nullable=True)
    improvement_suggestions = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="resumes")
