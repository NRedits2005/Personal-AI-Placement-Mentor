import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.resume import ResumeResponse
from backend.middleware.auth_middleware import get_current_user
from backend.models.student import Student
from backend.models.resume import Resume
from backend.services.agent_service import agent_service
from backend.config import settings

router = APIRouter(prefix="/api/resume", tags=["Resume Management"])

@router.post("/upload")
def upload_resume(
    file: UploadFile = File(...),
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Uploads a PDF resume and runs multi-agent onboarding (Resume, Skill Gap, Study Plan)."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Generate unique filename
    filename = f"{current_user.student_id}_{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)
    
    # Save file
    try:
        with open(filepath, "wb") as f:
            f.write(file.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded file: {e}")

    # Process multi-agent onboarding
    try:
        onboarding_result = agent_service.process_resume_onboarding(
            db=db,
            student_id=current_user.student_id,
            file_path=filepath,
            target_role=current_user.target_role or "AI Engineer",
            target_company=current_user.target_company
        )
        return {
            "message": "Resume uploaded and analyzed successfully.",
            "onboarding_results": {
                "resume_score": onboarding_result["resume_analysis"].get("resume_score", 0),
                "ats_score": onboarding_result["resume_analysis"].get("ats_score", 0),
                "skills": onboarding_result["resume_analysis"].get("skills", []),
                "missing_sections": onboarding_result["resume_analysis"].get("missing_sections", []),
                "improvement_suggestions": onboarding_result["resume_analysis"].get("improvement_suggestions", []),
                "skill_gaps": onboarding_result["skill_gaps"],
                "study_plan": onboarding_result["study_plan"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse and analyze resume: {e}")

@router.get("/active", response_model=ResumeResponse)
def get_active_resume(
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves the student's currently active resume analysis details."""
    resume = db.query(Resume).filter(Resume.student_id == current_user.student_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="No resume uploaded yet.")
    return resume
