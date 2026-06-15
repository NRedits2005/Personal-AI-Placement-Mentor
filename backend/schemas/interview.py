from pydantic import BaseModel
from datetime import datetime

class InterviewStartRequest(BaseModel):
    interview_type: str  # "HR" or "Technical"

class InterviewStartResponse(BaseModel):
    interview_id: int
    first_question: str

class InterviewAnswerRequest(BaseModel):
    answer: str

class InterviewAnswerResponse(BaseModel):
    score: int
    feedback: str
    next_question: str | None = None
    is_complete: bool = False

class MockInterviewResponse(BaseModel):
    interview_id: int
    student_id: int
    interview_type: str
    questions_answers: list[dict]
    score: float
    strengths: list[str]
    weaknesses: list[str]
    feedback: list[str]
    created_at: datetime

    class Config:
        from_attributes = True
