from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.auth import UserRegister, UserLogin, Token
from backend.schemas.student import StudentResponse
from backend.services.auth_service import AuthService
from backend.middleware.auth_middleware import get_current_user
from backend.models.student import Student

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Registers a new student profile."""
    return AuthService.register_student(db, user_data)

@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Logs in an existing student and yields a JWT token."""
    return AuthService.authenticate_student(db, login_data)

@router.post("/login-form", response_model=Token, include_in_schema=False)
def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """OAuth2 password flow login compatible with FastAPI Swagger UI docs."""
    login_data = UserLogin(email=form_data.username, password=form_data.password)
    return AuthService.authenticate_student(db, login_data)

@router.get("/me", response_model=StudentResponse)
def get_me(current_user: Student = Depends(get_current_user)):
    """Gets the current logged in user information."""
    return current_user
