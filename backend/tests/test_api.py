import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app
from backend.database import get_db, Base

# Set up clean in-memory database for unit testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply dependency override
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

def test_read_root(client):
    """Test standard main API root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_register_and_login(client):
    """Test user registration and subsequent token generation."""
    # 1. Register User
    reg_payload = {
        "email": "student1@example.com",
        "full_name": "Test Student One",
        "password": "securepassword123",
        "college": "Test College",
        "target_role": "AI Engineer"
    }
    reg_response = client.post("/api/auth/register", json=reg_payload)
    assert reg_response.status_code == 201
    assert reg_response.json()["email"] == "student1@example.com"
    
    # 2. Login User
    login_payload = {
        "email": "student1@example.com",
        "password": "securepassword123"
    }
    login_response = client.post("/api/api/auth/login" if False else "/api/auth/login", json=login_payload)
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert login_response.json()["token_type"] == "bearer"

def test_unauthorized_endpoints(client):
    """Ensure protected API paths block requests without headers."""
    protected_paths = [
        "/api/auth/me",
        "/api/skill-gap",
        "/api/roadmap",
        "/api/dashboard/summary"
    ]
    for path in protected_paths:
        response = client.get(path)
        assert response.status_code == 401
