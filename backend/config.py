import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/placement_prep"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # AI Models
    OPENAI_API_KEY: str = "mock-or-real-api-key"
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_BASE_URL: str | None = None
    
    # Security
    JWT_SECRET_KEY: str = "supersecretjwtkeychangeinproduction123456!"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # File Paths
    UPLOAD_DIR: str = "./uploads"
    REPORTS_DIR: str = "./reports"
    
    # Feedback Loops
    LOOP_RESUME_THRESHOLD: int = 85
    LOOP_INTERVIEW_THRESHOLD: int = 85

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instantiate settings
settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.REPORTS_DIR, exist_ok=True)
