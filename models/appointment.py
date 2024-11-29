from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Appointment(BaseModel):
    """
    Represents an appointment related to a pet. Contains details about 
    the appointment, including the pet, user, scheduled time, description, 
    and the current status of the appointment.
    """
    pet_id: str  # Foreign key for the pet
    type: str  # Type of the appointment
    doctor_name: Optional[str] = None
    clinic: Optional[str] = None
    description: Optional[str] = None  # Details about the appointment
    date_time: datetime  # Date and time of the appointment
    status: str  # Status of the appointment
        
    
class AppointmentUpdate(BaseModel):
    type: Optional[str] = None 
    doctor_name: Optional[str] = None
    clinic: Optional[str] = None
    description: Optional[str] = None # Appointment type can be updated
    date_time: Optional[datetime] = None       # Appointment date can be updated
    status: Optional[str] = None          # Appointment status an be updated