from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .infrastructure.database import get_db
from .infrastructure.repository import BookingRepository, TherapistRepository
from .infrastructure.sqs import SQSClient
from .core.models import Booking, BookingCreate, Therapist

app = FastAPI(
    title="Therapist Booking API",
    description="API for managing therapist bookings",
    version="1.0.0"
)

sqs_client = SQSClient()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/bookings", response_model=Booking)
async def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new booking.
    
    Args:
        booking: Booking details
        db: Database session
        
    Returns:
        Created booking
    """
    # Validate booking times
    if not booking.validate_times():
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time"
        )
    
    # Check if therapist exists
    therapist_repo = TherapistRepository(db)
    therapist = therapist_repo.get_by_id(booking.therapist_id)
    if not therapist:
        raise HTTPException(
            status_code=404,
            detail="Therapist not found"
        )
    
    # Create booking
    booking_repo = BookingRepository(db)
    created_booking = booking_repo.create(booking)
    
    # Send notification via SQS
    message = {
        "booking_id": created_booking.id,
        "therapist_id": created_booking.therapist_id,
        "client_email": created_booking.client_email,
        "start_time": created_booking.start_time.isoformat(),
        "end_time": created_booking.end_time.isoformat(),
        "event_type": "booking_created"
    }
    
    try:
        sqs_client.send_message(message)
    except Exception as e:
        # Log the error but don't fail the request
        print(f"Failed to send SQS message: {str(e)}")
    
    return created_booking

@app.get("/bookings/{booking_id}", response_model=Booking)
async def get_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    """
    Get booking by ID.
    
    Args:
        booking_id: ID of the booking to retrieve
        db: Database session
        
    Returns:
        Booking details
    """
    booking_repo = BookingRepository(db)
    booking = booking_repo.get_by_id(booking_id)
    
    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )
    
    return booking

@app.get("/therapists/{therapist_id}/bookings", response_model=List[Booking])
async def get_therapist_bookings(
    therapist_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all bookings for a therapist.
    
    Args:
        therapist_id: ID of the therapist
        db: Database session
        
    Returns:
        List of bookings
    """
    booking_repo = BookingRepository(db)
    return booking_repo.get_by_therapist(therapist_id)

@app.post("/therapists", response_model=Therapist)
async def create_therapist(
    therapist: Therapist,
    db: Session = Depends(get_db)
):
    """
    Create a new therapist.
    
    Args:
        therapist: Therapist details
        db: Database session
        
    Returns:
        Created therapist
    """
    therapist_repo = TherapistRepository(db)
    return therapist_repo.create(therapist)

@app.get("/therapists", response_model=List[Therapist])
async def list_therapists(
    db: Session = Depends(get_db)
):
    """
    List all therapists.
    
    Args:
        db: Database session
        
    Returns:
        List of therapists
    """
    therapist_repo = TherapistRepository(db)
    return therapist_repo.list_all()

@app.get("/therapists/{therapist_id}", response_model=Therapist)
async def get_therapist(
    therapist_id: int,
    db: Session = Depends(get_db)
):
    """
    Get therapist by ID.
    
    Args:
        therapist_id: ID of the therapist to retrieve
        db: Database session
        
    Returns:
        Therapist details
    """
    therapist_repo = TherapistRepository(db)
    therapist = therapist_repo.get_by_id(therapist_id)
    
    if not therapist:
        raise HTTPException(
            status_code=404,
            detail="Therapist not found"
        )
    
    return therapist 