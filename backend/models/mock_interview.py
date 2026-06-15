from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime, Float, String
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class MockInterview(Base):
    __tablename__ = "mock_interviews"

    interview_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    interview_type = Column(String(50), nullable=False)  # "HR" or "Technical"
    questions_answers = Column(JSON, default=list)  # List of objects: [{"question": "...", "answer": "...", "score": 80, "feedback": "..."}]
    score = Column(Float, default=0.0)
    strengths = Column(JSON, default=list)
    weaknesses = Column(JSON, default=list)
    feedback = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="mock_interviews")
