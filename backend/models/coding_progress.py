from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class CodingProgress(Base):
    __tablename__ = "coding_progress"

    progress_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    total_solved = Column(Integer, default=0)
    accuracy = Column(Float, default=0.0)
    weak_topics = Column(JSON, default=list)  # ["Trees", "Dynamic Programming"]
    solved_questions = Column(JSON, default=list)  # List of objects containing: {question_id, score, evaluation}
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="coding_progress")
