import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.services.db_service import init_db

# Import routers
from backend.routes.auth import router as auth_router
from backend.routes.student import router as student_router
from backend.routes.resume import router as resume_router
from backend.routes.skill_gap import router as skill_gap_router
from backend.routes.study_plan import router as study_plan_router
from backend.routes.coding import router as coding_router
from backend.routes.interview import router as interview_router
from backend.routes.github import router as github_router
from backend.routes.dashboard import router as dashboard_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI App
app = FastAPI(
    title="AI Placement Preparation Platform API",
    description="Multi-agent and MCP-integrated backend for customized placement training.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
def on_startup():
    logger.info("Starting up FastAPI application...")
    init_db()

# Register Routers
app.include_router(auth_router)
app.include_router(student_router)
app.include_router(resume_router)
app.include_router(skill_gap_router)
app.include_router(study_plan_router)
app.include_router(coding_router)
app.include_router(interview_router)
app.include_router(github_router)
app.include_router(dashboard_router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "AI Placement Preparation Platform Backend API",
        "documentation": "/docs"
    }
