from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from . import models
from ..core.models import Booking, BookingCreate, Therapist

class BookingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, booking: BookingCreate) -> Booking:
        db_booking = models.BookingModel(
            therapist_id=booking.therapist_id,
            client_name=booking.client_name,
            client_email=booking.client_email,
            start_time=booking.start_time,
            end_time=booking.end_time,
            status="pending"
        )
        self.db.add(db_booking)
        self.db.commit()
        self.db.refresh(db_booking)
        return Booking.from_orm(db_booking)

    def get_by_id(self, booking_id: int) -> Optional[Booking]:
        db_booking = self.db.query(models.BookingModel).filter(
            models.BookingModel.id == booking_id
        ).first()
        return Booking.from_orm(db_booking) if db_booking else None

    def get_by_therapist(self, therapist_id: int) -> List[Booking]:
        db_bookings = self.db.query(models.BookingModel).filter(
            models.BookingModel.therapist_id == therapist_id
        ).all()
        return [Booking.from_orm(booking) for booking in db_bookings]

class TherapistRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, therapist: Therapist) -> Therapist:
        db_therapist = models.TherapistModel(
            name=therapist.name,
            email=therapist.email,
            phone=therapist.phone
        )
        self.db.add(db_therapist)
        self.db.commit()
        self.db.refresh(db_therapist)
        return Therapist.from_orm(db_therapist)

    def get_by_id(self, therapist_id: int) -> Optional[Therapist]:
        db_therapist = self.db.query(models.TherapistModel).filter(
            models.TherapistModel.id == therapist_id
        ).first()
        return Therapist.from_orm(db_therapist) if db_therapist else None

    def list_all(self) -> List[Therapist]:
        db_therapists = self.db.query(models.TherapistModel).all()
        return [Therapist.from_orm(therapist) for therapist in db_therapists] 