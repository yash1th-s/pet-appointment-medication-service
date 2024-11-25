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
    
    
    
@router.put("/{reminder_id}")
async def update_reminder_endpoint(reminder_id: int, reminder_data: ReminderUpdate):
    """
    API endpoint to update a recurring reminder.
    """
    try:
        # Update the reminder details using the service layer
        reminder_service.update_reminder_details(reminder_id, reminder_data.dict(exclude_unset=True))
        return {"message": "Reminder updated successfully"}
    except ValueError as e:
        # If the reminder is not found, return a 404 error
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Handle other unexpected errors
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{reminder_id}")
async def delete_reminder_endpoint(reminder_id: int):
    """
    API endpoint to delete a recurring reminder.
    """
    try:
        # Call the service layer to remove the reminder
        reminder_service.remove_reminder(reminder_id)
        return {"message": "Reminder deleted successfully"}
    except ValueError as e:
        # Return a 404 error if the reminder is not found
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Handle other unexpected errors
        raise HTTPException(status_code=500, detail="An error occurred while deleting the reminder")


user_reminders_router = APIRouter()

@user_reminders_router.get("/user/{user_id}/reminders")
async def get_user_reminders_endpoint(user_id: int):
    """
    API endpoint to retrieve all reminders for a specific user.
    """
    try:
        # Call the service layer to fetch reminders
        reminders = reminder_service.get_user_reminders(user_id)
        return {"reminders": reminders}
    except ValueError as e:
        # Return a 404 error if no reminders are found
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Handle other unexpected errors
        raise HTTPException(status_code=500, detail="An error occurred while retrieving reminders")
