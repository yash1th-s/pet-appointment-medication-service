# api/appointments.py
from fastapi import APIRouter, HTTPException
from models.reminder import Reminder, ReminderUpdate
from services import reminder_service


router = APIRouter()

@router.post("/", status_code=201)
async def create_reminder_endpoint(reminder: Reminder):
    """
    API endpoint to create a new recurring reminder.
    """
    try:
        reminder_id = reminder_service.add_reminder(reminder)
        return {"message": "Reminder created successfully", "reminder_id": reminder_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/{reminder_id}")
async def get_reminder_endpoint(reminder_id: int):
    """
    API endpoint to retrieve details of a specific reminder.
    """
    try:
        reminder = reminder_service.get_reminder_details(reminder_id)
        return {"reminder": reminder}
    except ValueError as e:
        # If the reminder is not found, return a 404 error
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Handle other unexpected errors
        raise HTTPException(status_code=500, detail=str(e))
