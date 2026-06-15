from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.coding import CodingQuestionResponse, CodingSubmissionRequest, CodingEvaluationResponse, CodingProgressResponse
from backend.middleware.auth_middleware import get_current_user
from backend.models.student import Student
from backend.models.coding_progress import CodingProgress
from backend.services.agent_service import agent_service

router = APIRouter(prefix="/api/coding", tags=["Coding Practice"])

@router.get("/question", response_model=CodingQuestionResponse)
def get_coding_question(
    difficulty: str = "Medium",
    topic: str | None = None,
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generates a personalized DSA coding question based on difficulty and topic."""
    # Generate question
    question = agent_service.coding_agent.generate_question(
        difficulty=difficulty,
        topic=topic,
        target_company=current_user.target_company
    )
    return question

@router.post("/submit", response_model=CodingEvaluationResponse)
def submit_solution(
    req: CodingSubmissionRequest,
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submits code solution, runs LLM evaluator, and logs progress."""
    # Fetch details of question to evaluate context correctly
    question_details = agent_service.coding_agent.generate_question(
        topic=req.question_id,
        target_company=current_user.target_company
    )
    # Ensure ID matches
    question_details["question_id"] = req.question_id
    
    evaluation = agent_service.submit_coding_solution(
        db=db,
        student_id=current_user.student_id,
        question_details=question_details,
        code=req.code
    )
    return evaluation

@router.get("/progress", response_model=CodingProgressResponse)
def get_progress(
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves coding analytics and history of solved questions."""
    progress = db.query(CodingProgress).filter(CodingProgress.student_id == current_user.student_id).first()
    if not progress:
        # Return empty default response
        return CodingProgressResponse(
            progress_id=0,
            student_id=current_user.student_id,
            total_solved=0,
            accuracy=0.0,
            weak_topics=[],
            solved_questions=[],
            created_at=datetime.utcnow() # Wait, datetime not imported, let's make sure it is imported or just return a default
        )
    return progress
