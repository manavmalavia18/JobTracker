import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from app.main import app
from app.database import get_session

@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def client(session):
    def get_session_override():
        yield session
    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_and_get_job(client):
    job_data = {
        "title": "DevOps Engineer",
        "company": "TestCorp",
        "location": "Remote",
        "description": "Test job description",
        "url": "https://example.com/job/1"
    }
    response = client.post("/jobs", json=job_data)
    assert response.status_code == 200
    assert response.json()["title"] == "DevOps Engineer"

    response = client.get("/jobs")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_filter_jobs_by_location(client):
    job_data = {
        "title": "Backend Engineer",
        "company": "TestCorp",
        "location": "London",
        "description": "Test job",
        "url": "https://example.com/job/2"
    }
    client.post("/jobs", json=job_data)
    response = client.get("/jobs?location=London")
    assert response.status_code == 200
    assert all("London" in job["location"] for job in response.json())