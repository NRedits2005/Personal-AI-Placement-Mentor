from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.middleware.auth_middleware import get_current_user
from backend.models.student import Student
from backend.models.resume import Resume
from backend.models.coding_progress import CodingProgress
from backend.models.mock_interview import MockInterview
from backend.models.readiness_score import ReadinessScore
from backend.models.github_project import GitHubProject

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/summary")
def get_dashboard_summary(
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves placement analytics and metric indicators for the dashboard."""
    # 1. Resume metrics
    resume = db.query(Resume).filter(Resume.student_id == current_user.student_id).first()
    resume_score = resume.resume_score if resume else 0
    ats_score = resume.ats_score if resume else 0
    
    # 2. Coding metrics
    coding = db.query(CodingProgress).filter(CodingProgress.student_id == current_user.student_id).first()
    coding_solved = coding.total_solved if coding else 0
    coding_accuracy = coding.accuracy if coding else 0.0
    
    # 3. Interview metrics
    interviews = db.query(MockInterview).filter(MockInterview.student_id == current_user.student_id).all()
    hr_count = sum(1 for i in interviews if i.interview_type == "HR")
    tech_count = sum(1 for i in interviews if i.interview_type == "Technical")
    
    hr_scores = [i.score for i in interviews if i.interview_type == "HR"]
    avg_hr_score = sum(hr_scores) / len(hr_scores) if hr_scores else 0.0
    
    tech_scores = [i.score for i in interviews if i.interview_type == "Technical"]
    avg_tech_score = sum(tech_scores) / len(tech_scores) if tech_scores else 0.0
    
    # 4. Project metrics
    project_count = db.query(GitHubProject).filter(GitHubProject.student_id == current_user.student_id).count()
    
    # 5. Readiness Score History (max last 7 records for trending charts)
    readiness_history = db.query(ReadinessScore).filter(
        ReadinessScore.student_id == current_user.student_id
    ).order_by(ReadinessScore.created_at.asc()).all()
    
    readiness_trend = []
    for r in readiness_history[-7:]:
        readiness_trend.append({
            "overall_score": round(r.overall_score, 1),
            "resume_score": round(r.resume_weight_score, 1),
            "coding_score": round(r.coding_weight_score, 1),
            "technical_score": round(r.technical_weight_score, 1),
            "hr_score": round(r.hr_weight_score, 1),
            "project_score": round(r.project_weight_score, 1),
            "timestamp": r.created_at.isoformat()
        })
        
    latest_score = readiness_trend[-1]["overall_score"] if readiness_trend else 0.0

    return {
        "student_name": current_user.full_name,
        "target_role": current_user.target_role or "Not set",
        "target_company": current_user.target_company or "Not set",
        "resume": {
            "resume_score": resume_score,
            "ats_score": ats_score,
            "has_resume": resume is not None
        },
        "coding": {
            "solved": coding_solved,
            "accuracy": coding_accuracy
        },
        "interviews": {
            "hr_count": hr_count,
            "tech_count": tech_count,
            "avg_hr_score": avg_hr_score,
            "avg_tech_score": avg_tech_score
        },
        "projects": {
            "count": project_count
        },
        "latest_readiness_score": latest_score,
        "readiness_trend": readiness_trend
    }
