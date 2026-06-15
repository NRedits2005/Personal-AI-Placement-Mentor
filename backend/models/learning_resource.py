from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class LearningResource(Base):
    __tablename__ = "learning_resources"

    resource_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    topic = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    url = Column(String(500), nullable=True)
    resource_type = Column(String(50), nullable=True)  # "Video", "Article", "Course"
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="learning_resources")
