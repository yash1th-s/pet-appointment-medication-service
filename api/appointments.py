# api/appointments.py
from fastapi import APIRouter, HTTPException
from models.appointment import Appointment, AppointmentUpdate
from services import appointment_service

router = APIRouter()

@router.post("/", status_code=201)
async def create_appointment_endpoint(appointment: Appointment):
    try:
        # Call the service layer to handle appointment scheduling
        appointment_service.schedule_appointment(appointment)
        return {"message": "Appointment scheduled successfully", "appointment": appointment.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{appointment_id}")
async def get_appointment_endpoint(appointment_id: int):
    try:
        # Get the appointment details using the service layer
        appointment = appointment_service.get_appointment_details(appointment_id)
        return {"appointment": appointment.dict()}
    except ValueError as e:
        # If appointment not found, return a 404 error
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Handle any other errors
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.put("/{appointment_id}")
async def update_appointment_endpoint(appointment_id: int, appointment: AppointmentUpdate):
    try:
        # Update the appointment details using the service layer
        appointment_service.update_appointment_details(appointment_id, appointment)
        return {"message": "Appointment updated successfully"}
    except ValueError as e:
        # Return a 404 error if the appointment was not found
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Handle other errors (e.g., database issues)
        raise HTTPException(status_code=500, detail="An error occurred while updating the appointment")
    
    
@router.delete("/{appointment_id}")
async def cancel_appointment_endpoint(appointment_id: int):
    try:
        # Call the service layer to cancel the appointment
        appointment_service.cancel_appointment(appointment_id)
        return {"message": "Appointment canceled successfully"}
    except ValueError as e:
        # If the appointment wasn't found, return a 404 error
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Handle other errors (e.g., database issues)
        raise HTTPException(status_code=500, detail="An error occurred while canceling the appointment")


@router.get("/user/{user_id}/appointments")
async def get_user_appointments(user_id: int):
    try:
        # Get all upcoming appointments for the user
        appointments = appointment_service.get_upcoming_appointments(user_id)
        return {"appointments": appointments}
    except ValueError as e:
        # Return a 404 error if no upcoming appointments are found
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Handle other errors (e.g., database issues)
        raise HTTPException(status_code=500, detail="An error occurred while retrieving appointments")
    

@router.get("/pet/{pet_id}/appointments")
async def get_pet_appointments(pet_id: int):
    try:
        # Get all upcoming appointments for the pet
        appointments = appointment_service.get_appointments_for_pet(pet_id)
        return {"appointments": appointments}
    except ValueError as e:
        # Return a 404 error if no upcoming appointments are found
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Handle other errors (e.g., database issues)
        raise HTTPException(status_code=500, detail="An error occurred while retrieving appointments")