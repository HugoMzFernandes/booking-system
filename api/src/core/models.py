from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class Therapist(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    created_at: Optional[datetime] = None

class Booking(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: Optional[int] = None
    therapist_id: int
    client_name: str = Field(..., min_length=1, max_length=100)
    client_email: EmailStr
    start_time: datetime
    end_time: datetime
    status: str = Field(default="pending", pattern="^(pending|confirmed|cancelled)$")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def validate_times(self) -> bool:
        """Validate that end_time is after start_time."""
        return self.end_time > self.start_time

class BookingCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    therapist_id: int
    client_name: str = Field(..., min_length=1, max_length=100)
    client_email: EmailStr
    start_time: datetime
    end_time: datetime

    def validate_times(self) -> bool:
        """Validate that end_time is after start_time."""
        return self.end_time > self.start_time 