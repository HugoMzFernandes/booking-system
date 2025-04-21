import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import app
from src.infrastructure.database import Base, get_db
from src.infrastructure.models import TherapistModel, BookingModel

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # Don't close the session here
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def test_therapist(db_session):
    therapist = TherapistModel(
        name="Test Therapist",
        email="therapist@test.com"
    )
    db_session.add(therapist)
    db_session.commit()
    db_session.refresh(therapist)
    return therapist

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_booking(client, test_therapist, db_session):
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    
    booking_data = {
        "therapist_id": test_therapist.id,
        "client_name": "Test Client",
        "client_email": "client@test.com",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat()
    }
    
    response = client.post("/bookings", json=booking_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["therapist_id"] == test_therapist.id
    assert data["client_name"] == "Test Client"
    assert data["client_email"] == "client@test.com"
    assert data["status"] == "pending"

def test_create_booking_invalid_times(client, test_therapist):
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time - timedelta(hours=1)  # End time before start time
    
    booking_data = {
        "therapist_id": test_therapist.id,
        "client_name": "Test Client",
        "client_email": "client@test.com",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat()
    }
    
    response = client.post("/bookings", json=booking_data)
    assert response.status_code == 400
    assert "End time must be after start time" in response.json()["detail"]

def test_create_booking_invalid_therapist(client):
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    
    booking_data = {
        "therapist_id": 999,  # Non-existent therapist
        "client_name": "Test Client",
        "client_email": "client@test.com",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat()
    }
    
    response = client.post("/bookings", json=booking_data)
    assert response.status_code == 404
    assert "Therapist not found" in response.json()["detail"]

def test_get_booking(client, test_therapist, db_session):
    # Create a booking first
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    
    booking = BookingModel(
        therapist_id=test_therapist.id,
        client_name="Test Client",
        client_email="client@test.com",
        start_time=start_time,
        end_time=end_time,
        status="pending"
    )
    db_session.add(booking)
    db_session.commit()
    db_session.refresh(booking)
    
    response = client.get(f"/bookings/{booking.id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == booking.id
    assert data["therapist_id"] == test_therapist.id
    assert data["client_name"] == "Test Client"

def test_get_nonexistent_booking(client):
    response = client.get("/bookings/999")
    assert response.status_code == 404
    assert "Booking not found" in response.json()["detail"]

def test_get_therapist_bookings(client, test_therapist, db_session):
    # Create multiple bookings
    start_time = datetime.now() + timedelta(days=1)
    bookings = []
    
    for i in range(3):
        end_time = start_time + timedelta(hours=1)
        booking = BookingModel(
            therapist_id=test_therapist.id,
            client_name=f"Test Client {i}",
            client_email=f"client{i}@test.com",
            start_time=start_time,
            end_time=end_time,
            status="pending"
        )
        db_session.add(booking)
        bookings.append(booking)
        start_time = end_time
    
    db_session.commit()
    
    response = client.get(f"/therapists/{test_therapist.id}/bookings")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 3
    assert all(b["therapist_id"] == test_therapist.id for b in data) 