from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class GitHubProject(Base):
    __tablename__ = "github_projects"

    project_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    repo_name = Column(String(100), nullable=False)
    repo_url = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    languages = Column(JSON, default=dict)  # {"Python": 80.5, "HTML": 19.5}
    stars = Column(Integer, default=0)
    metadata_info = Column(JSON, default=dict)  # Renamed from metadata to avoid SQLAlchemy conflicts
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="github_projects")
