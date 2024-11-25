from db.crud import create_reminder, get_reminder_by_id
from models.reminder import Reminder
from fastapi import HTTPException


def add_reminder(reminder: Reminder) -> int:
    """
    Calls the CRUD function to create a reminder.
    Returns the ID of the created reminder.
    """
    try:
        reminder_id = create_reminder(reminder)
        return reminder_id
    except Exception as e:
        raise RuntimeError(f"Failed to add reminder: {e}")
    
    
def get_reminder_details(reminder_id: int) -> dict:
    """
    Fetches details of a specific reminder.
    Raises an error if the reminder does not exist.
    """
    reminder = get_reminder_by_id(reminder_id)
    if not reminder:
        raise ValueError(f"Reminder with ID {reminder_id} not found.")
    return reminder