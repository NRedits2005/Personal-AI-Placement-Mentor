from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
from backend.models.student import Student
from backend.schemas.auth import UserRegister, UserLogin, Token
from backend.utils.hashing import hash_password, verify_password
from backend.utils.jwt_helper import create_access_token
from backend.config import settings

class AuthService:
    @staticmethod
    def register_student(db: Session, reg_data: UserRegister) -> Student:
        """Registers a new student, verifying email uniqueness and hashing the password."""
        # Check if email exists
        existing = db.query(Student).filter(Student.email == reg_data.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered"
            )
            
        hashed = hash_password(reg_data.password)
        new_student = Student(
            full_name=reg_data.full_name,
            email=reg_data.email,
            password_hash=hashed,
            college=reg_data.college,
            department=reg_data.department,
            graduation_year=reg_data.graduation_year,
            target_role=reg_data.target_role,
            target_company=reg_data.target_company
        )
        
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return new_student

    @staticmethod
    def authenticate_student(db: Session, login_data: UserLogin) -> Token:
        """Validates credentials and returns a JWT access token."""
        student = db.query(Student).filter(Student.email == login_data.email).first()
        if not student or not verify_password(login_data.password, student.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Create token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": student.email, "student_id": student.student_id},
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")
