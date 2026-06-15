from pydantic import BaseModel
from datetime import datetime

class CodingQuestionResponse(BaseModel):
    question_id: str
    title: str
    description: str
    difficulty: str  # "Easy", "Medium", "Hard"
    company_tags: list[str]
    sample_input: str
    sample_output: str
    constraints: str

class CodingSubmissionRequest(BaseModel):
    question_id: str
    code: str
    language: str = "python"

class CodingEvaluationResponse(BaseModel):
    score: int
    time_complexity: str
    space_complexity: str
    feedback: str
    passed: bool
    suggestions: list[str] = []

class CodingProgressResponse(BaseModel):
    progress_id: int
    student_id: int
    total_solved: int
    accuracy: float
    weak_topics: list[str]
    solved_questions: list[dict]
    created_at: datetime

    class Config:
        from_attributes = True
