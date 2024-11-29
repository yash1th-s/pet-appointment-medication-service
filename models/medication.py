from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Medication(BaseModel):
    """
    Represents a medication schedule for a pet. Contains details about 
    the medication, its dosage, frequency, and start/end dates.
    """
    name: str  # Name of the medication
    dosage: str  # Dosage instructions (e.g., "1 tablet", "5 ml")
    frequency: str  # Frequency of the medication (e.g., "Once daily", "Twice weekly")
    start_date: datetime  # Start date for the medication
    end_date: Optional[datetime] = None  # End date for the medication
    notes: Optional[str] = None  # Additional details or instructions


class MedicationReminder(BaseModel):
    """
    Represents a reminder for a specific medication dose.
    """
    medication_id: int  # Foreign key for the medication
    reminder_time: datetime  # Time for the reminder
    message: Optional[str] = Field(default="It's time to take your medication!")  # Custom message
    
    
class MedicationOut(BaseModel):
    """
    Represents the output data for a medication schedule. This is the format 
    that will be returned in the response after the medication is created.
    """
    medication_id: int
    pet_id: str
    name: str
    dosage: str
    frequency: str
    start_date: datetime
    end_date: Optional[datetime] = None
    notes: Optional[str] = None
    
    
class MedicationUpdate(BaseModel):
    name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    start_date: Optional[str] = None  # ISO-8601 format
    end_date: Optional[str] = None  # ISO-8601 format
    notes: Optional[str] = None
