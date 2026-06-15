from pydantic import BaseModel
from datetime import datetime

class SkillStatus(BaseModel):
    skill: str
    status: str  # "Missing", "Present"
    priority: str  # "High", "Medium", "Low"

class SkillGapBase(BaseModel):
    skills: list[SkillStatus]

class SkillGapResponse(SkillGapBase):
    gap_id: int
    student_id: int
    created_at: datetime

    class Config:
        from_attributes = True
