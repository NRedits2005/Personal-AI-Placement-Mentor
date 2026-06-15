from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.middleware.auth_middleware import get_current_user
from backend.models.student import Student
from backend.models.github_project import GitHubProject
from backend.mcp.client import MCPClient
from backend.services.agent_service import agent_service

router = APIRouter(prefix="/api/github", tags=["GitHub Analyzer"])

@router.post("/analyze")
def analyze_github_profile(
    github_url: str | None = None,
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Fetches repositories for a GitHub profile and logs metadata in DB."""
    mcp_client = MCPClient()
    
    url_to_use = github_url or current_user.target_company # Fallback/Check
    if not url_to_use:
        # Check active resume for github url
        from backend.models.resume import Resume
        active_resume = db.query(Resume).filter(Resume.student_id == current_user.student_id).first()
        if active_resume and active_resume.github_url:
            url_to_use = active_resume.github_url
            
    if not url_to_use:
        raise HTTPException(
            status_code=400, 
            detail="GitHub URL not provided and not found in your uploaded resume."
        )

    try:
        repos = mcp_client.analyze_github(url_to_use)
        
        # Clear existing repos for this student to rebuild list
        db.query(GitHubProject).filter(GitHubProject.student_id == current_user.student_id).delete()
        
        saved_projects = []
        for repo in repos:
            # Classify if project is related to target_role
            role_lower = (current_user.target_role or "AI Engineer").lower()
            repo_name_lower = repo.get("name", "").lower()
            desc_lower = (repo.get("description") or "").lower()
            lang_lower = (repo.get("language") or "").lower()
            
            ai_keywords = ["ai", "ml", "machine learning", "deep learning", "neural", "llm", "rag", "nlp", "computer vision", "recommend", "data", "model", "prediction", "tensor", "torch", "sklearn", "keras"]
            frontend_keywords = ["frontend", "react", "vue", "angular", "css", "html", "tailwind", "ui", "ux", "javascript", "typescript", "sass", "web"]
            backend_keywords = ["backend", "api", "fastapi", "django", "flask", "springboot", "express", "node", "database", "postgres", "sql", "redis", "docker", "graphql", "server", "microservice", "spring"]
            
            is_related = False
            if "ai" in role_lower or "machine" in role_lower or "data" in role_lower or "scientist" in role_lower:
                is_related = any(k in repo_name_lower or k in desc_lower for k in ai_keywords) or lang_lower in ["python", "r", "julia"]
            elif "frontend" in role_lower or "web" in role_lower:
                is_related = any(k in repo_name_lower or k in desc_lower for k in frontend_keywords) or lang_lower in ["javascript", "typescript", "html", "css"]
            elif "backend" in role_lower or "software" in role_lower:
                is_related = any(k in repo_name_lower or k in desc_lower for k in backend_keywords) or lang_lower in ["python", "go", "java", "c#", "c++", "rust"]
            elif "full" in role_lower or "stack" in role_lower or "developer" in role_lower:
                # Full stack matches frontend or backend keywords
                is_related = any(k in repo_name_lower or k in desc_lower for k in frontend_keywords + backend_keywords) or lang_lower in ["javascript", "typescript", "python", "go", "java", "html", "css"]
            else:
                is_related = any(k in repo_name_lower or k in desc_lower for k in ["code", "system", "app", "project", "algorithm"])

            metadata = repo.copy()
            metadata["is_role_related"] = is_related

            db_project = GitHubProject(
                student_id=current_user.student_id,
                repo_name=repo.get("name"),
                repo_url=repo.get("url"),
                description=repo.get("description"),
                languages={repo.get("language"): 100} if repo.get("language") else {},
                stars=repo.get("stars", 0),
                metadata_info=metadata
            )
            db.add(db_project)
            saved_projects.append({
                "name": db_project.repo_name,
                "url": db_project.repo_url,
                "stars": db_project.stars,
                "description": db_project.description,
                "is_role_related": is_related
            })
            
        db.commit()
        
        # Update AI Readiness (recalculates weighted projects score)
        agent_service.calculate_readiness_score(db, current_user.student_id)
        
        return {
            "message": "GitHub profile analyzed successfully.",
            "projects_found": saved_projects
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch repositories: {e}")

@router.get("/projects")
def get_github_projects(
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves already analyzed GitHub repositories of the student."""
    projects = db.query(GitHubProject).filter(GitHubProject.student_id == current_user.student_id).all()
    return projects
