from pydantic import BaseModel
from datetime import datetime

class ResumeBase(BaseModel):
    resume_path: str
    resume_score: int
    ats_score: int
    extracted_skills: list[str]
    github_url: str | None = None
    linkedin_url: str | None = None
    improvement_suggestions: list[str]

class ResumeResponse(ResumeBase):
    resume_id: int
    student_id: int
    created_at: datetime

    class Config:
        from_attributes = True
