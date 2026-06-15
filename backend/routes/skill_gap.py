from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.skill_gap import SkillGapResponse
from backend.middleware.auth_middleware import get_current_user
from backend.models.student import Student
from backend.models.skill_gap import SkillGap

router = APIRouter(prefix="/api/skill-gap", tags=["Skill Gap Analysis"])

@router.get("", response_model=SkillGapResponse)
def get_skill_gap(
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves the prioritised list of skill gaps for the student."""
    gap = db.query(SkillGap).filter(SkillGap.student_id == current_user.student_id).first()
    if not gap:
        raise HTTPException(status_code=404, detail="No skill gap analysis found. Please upload a resume first.")
    return gap
