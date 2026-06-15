from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.interview import InterviewStartRequest, InterviewStartResponse, InterviewAnswerRequest, InterviewAnswerResponse, MockInterviewResponse
from backend.middleware.auth_middleware import get_current_user
from backend.models.student import Student
from backend.models.mock_interview import MockInterview
from backend.services.agent_service import agent_service
from backend.redis_client import redis_client

router = APIRouter(prefix="/api/interview", tags=["Mock Interview"])

@router.post("/start", response_model=InterviewStartResponse)
def start_interview(
    req: InterviewStartRequest,
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Starts a new mock interview session and returns the first question."""
    if req.interview_type not in ["HR", "Technical"]:
        raise HTTPException(status_code=400, detail="Invalid interview type. Must be HR or Technical.")
    
    result = agent_service.start_mock_interview(
        db=db,
        student_id=current_user.student_id,
        interview_type=req.interview_type
    )
    return result

@router.post("/{interview_id}/answer", response_model=InterviewAnswerResponse)
def submit_answer(
    interview_id: int,
    req: InterviewAnswerRequest,
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submits answer to the current question, evaluates, and returns the next question or completes the interview."""
    try:
        result = agent_service.submit_interview_answer(
            db=db,
            student_id=current_user.student_id,
            interview_id=interview_id,
            answer=req.answer
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/active-chat")
def get_active_chat(current_user: Student = Depends(get_current_user)):
    """Retrieves conversation turns of the active interview cached in Redis."""
    chat = redis_client.get_conversation_history(current_user.student_id, category="interview")
    active_type = redis_client.get(f"interview_type:{current_user.student_id}") or "Interview"
    return {"interview_type": active_type, "history": chat}

@router.get("/history", response_model=list[MockInterviewResponse])
def get_history(
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves list of completed mock interviews."""
    interviews = db.query(MockInterview).filter(MockInterview.student_id == current_user.student_id).all()
    return interviews
