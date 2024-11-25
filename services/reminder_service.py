from db.crud import create_reminder, get_reminder_by_id, update_reminder, delete_reminder, get_reminders_by_user
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


def update_reminder_details(reminder_id: int, reminder_data: dict):
    """
    Updates a recurring reminder's details.
    Raises an error if the reminder does not exist.
    """
    try:
        update_reminder(reminder_id, reminder_data)
    except ValueError as e:
        raise ValueError(str(e))
    
    
    
def remove_reminder(reminder_id: int):
    """
    Removes a recurring reminder by ID.
    Raises an error if the reminder does not exist.
    """
    try:
        delete_reminder(reminder_id)
    except ValueError as e:
        raise ValueError(str(e))
    
    
def get_user_reminders(user_id: int):
    """
    Service function to retrieve all reminders for a specific user.
    """
    reminders = get_reminders_by_user(user_id)
    if not reminders:
        raise ValueError(f"No reminders found for user with ID {user_id}.")
    return reminders