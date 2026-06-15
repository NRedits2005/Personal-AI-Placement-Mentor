from pydantic import BaseModel
from datetime import datetime

class TaskItem(BaseModel):
    task: str
    completed: bool = False

class StudyPlanResponse(BaseModel):
    plan_id: int
    student_id: int
    tasks: dict[str, list[TaskItem]]  # e.g., {"Week 1": [TaskItem, TaskItem]}
    completion_percentage: float
    created_at: datetime

    class Config:
        from_attributes = True

class UpdateTaskRequest(BaseModel):
    week: str
    task_index: int
    completed: bool
