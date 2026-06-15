from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    college = Column(String(255), nullable=True)
    department = Column(String(255), nullable=True)
    graduation_year = Column(Integer, nullable=True)
    target_role = Column(String(100), nullable=True)
    target_company = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    resumes = relationship("Resume", back_populates="student", cascade="all, delete-orphan")
    skill_gaps = relationship("SkillGap", back_populates="student", cascade="all, delete-orphan")
    study_plans = relationship("StudyPlan", back_populates="student", cascade="all, delete-orphan")
    coding_progress = relationship("CodingProgress", back_populates="student", cascade="all, delete-orphan")
    mock_interviews = relationship("MockInterview", back_populates="student", cascade="all, delete-orphan")
    readiness_scores = relationship("ReadinessScore", back_populates="student", cascade="all, delete-orphan")
    github_projects = relationship("GitHubProject", back_populates="student", cascade="all, delete-orphan")
    learning_resources = relationship("LearningResource", back_populates="student", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="student", cascade="all, delete-orphan")
    agent_logs = relationship("AgentLog", back_populates="student", cascade="all, delete-orphan")
