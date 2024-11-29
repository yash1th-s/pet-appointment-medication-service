from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Reminder(BaseModel):
    """
    Represents a recurring reminder. Includes details about the reminder
    and its schedule.
    """
    title: str  # Title of the reminder (e.g., "Monthly Flea Prevention")
    description: Optional[str] = None  # Additional details about the reminder
    frequency: str  # Frequency of the reminder (e.g., "monthly", "weekly")
    start_date: datetime  # Start date for the reminder
    end_date: Optional[datetime] = None  # End date for the reminder (if applicable)
    status: Optional[str] = "active"  # Status of the reminder (e.g., "active", "inactive")

class ReminderUpdate(BaseModel):
    """
    Represents fields that can be updated for a recurring reminder.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None
