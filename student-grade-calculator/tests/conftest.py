"""
Test fixtures for the Student Grade Calculator API.

Provides a test database, test client, and helper fixtures
that create isolated test environments for each test function.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Provide a test database session."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_database():
    """Create fresh tables for each test and tear down after."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    """Provide a test client with the test database dependency override."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def sample_student():
    """Return sample student data."""
    return {"student_id": "STU001", "name": "Alice Johnson"}


@pytest.fixture
def sample_score():
    """Return sample score data."""
    return {"subject": "Mathematics", "score": 95}


@pytest.fixture
def client_with_student(client, sample_student):
    """Provide a test client with one student already created."""
    client.post("/api/students", json=sample_student)
    return client


@pytest.fixture
def client_with_data(client):
    """Provide a test client with multiple students and scores for report testing."""
    students = [
        {"student_id": "STU001", "name": "Alice Johnson"},
        {"student_id": "STU002", "name": "Bob Smith"},
        {"student_id": "STU003", "name": "Charlie Brown"},
    ]
    scores = [
        # Alice - high performer
        {"student_id": "STU001", "subject": "Mathematics", "score": 95},
        {"student_id": "STU001", "subject": "Physics", "score": 88},
        {"student_id": "STU001", "subject": "Chemistry", "score": 92},
        # Bob - average performer
        {"student_id": "STU002", "subject": "Mathematics", "score": 72},
        {"student_id": "STU002", "subject": "Physics", "score": 68},
        {"student_id": "STU002", "subject": "Chemistry", "score": 75},
        # Charlie - good performer
        {"student_id": "STU003", "subject": "Mathematics", "score": 85},
        {"student_id": "STU003", "subject": "Physics", "score": 90},
        {"student_id": "STU003", "subject": "Chemistry", "score": 78},
    ]

    for student in students:
        client.post("/api/students", json=student)

    for score in scores:
        sid = score["student_id"]
        client.post(
            f"/api/students/{sid}/scores",
            json={"subject": score["subject"], "score": score["score"]},
        )

    return client
