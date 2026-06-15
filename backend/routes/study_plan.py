from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.study_plan import StudyPlanResponse, UpdateTaskRequest
from backend.middleware.auth_middleware import get_current_user
from backend.models.student import Student
from backend.services.agent_service import agent_service

router = APIRouter(prefix="/api/roadmap", tags=["Study Roadmap"])

@router.get("", response_model=StudyPlanResponse)
def get_roadmap(
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves the personalized weekly study plan roadmap."""
    plan = agent_service.get_study_plan(db, current_user.student_id)
    if not plan:
        raise HTTPException(status_code=404, detail="No study roadmap found. Please upload a resume first.")
    return plan

@router.put("/task", response_model=StudyPlanResponse)
def update_task(
    req: UpdateTaskRequest,
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Updates completion status of a study plan task item."""
    try:
        updated_plan = agent_service.update_task_progress(
            db=db,
            student_id=current_user.student_id,
            week=req.week,
            task_index=req.task_index,
            completed=req.completed
        )
        return updated_plan
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
