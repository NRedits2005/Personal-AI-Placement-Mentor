from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.student import StudentResponse, StudentUpdate
from backend.middleware.auth_middleware import get_current_user
from backend.models.student import Student

router = APIRouter(prefix="/api/student", tags=["Student Profile"])

@router.put("/profile", response_model=StudentResponse)
def update_profile(
    update_data: StudentUpdate,
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Updates the student profile details."""
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user
