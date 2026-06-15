from pydantic import BaseModel, EmailStr
from datetime import datetime

class StudentBase(BaseModel):
    full_name: str
    email: EmailStr
    college: str | None = None
    department: str | None = None
    graduation_year: int | None = None
    target_role: str | None = None
    target_company: str | None = None

class StudentUpdate(BaseModel):
    full_name: str | None = None
    college: str | None = None
    department: str | None = None
    graduation_year: int | None = None
    target_role: str | None = None
    target_company: str | None = None

class StudentResponse(StudentBase):
    student_id: int
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True
        # orm_mode is for older pydantic but we support both from_attributes and orm_mode for maximum compatibility.
