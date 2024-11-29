# api/appointments.py
from fastapi import APIRouter, HTTPException
from models.medication import Medication, MedicationOut, MedicationUpdate
from services import medication_service


router = APIRouter()


@router.post("/pet/{pet_id}/medication", status_code=201)
async def create_medication_endpoint(pet_id: str, medication: Medication):
    try:
        
        # Call the service layer to handle the logic
        medication_id = medication_service.add_medication(pet_id, medication)
        return {"message": "Medication added successfully", "medication_id": medication_id}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred while adding the medication.")
    
    
@router.get("/pet/{pet_id}/medications")
async def get_pet_medications(pet_id: str):
    try:
        # Get all medication schedules for the pet
        medications = medication_service.get_medications_for_pet(pet_id)
        return {"medications": medications}
    except ValueError as e:
        # Return a 404 error if no medications are found
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Handle any other errors (e.g., database issues)
        raise HTTPException(status_code=500, detail="An error occurred while retrieving medications")
    

@router.put("/pet/{pet_id}/medication/{medication_id}")
async def update_medication_endpoint(pet_id: str, medication_id: int, medication_update: MedicationUpdate):
    try:
        # Convert the MedicationUpdate object to a dictionary and remove None values
        update_data = {key: value for key, value in medication_update.dict().items() if value is not None}

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields provided to update")

        # Call the service layer to update the medication schedule
        medication_service.update_medication_schedule(medication_id, update_data)

        return {"message": "Medication updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
    
@router.delete("/pet/{pet_id}/medication/{medication_id}", status_code=200)
async def delete_medication_endpoint(pet_id: str, medication_id: int):
    """
    Endpoint to delete a medication schedule for a pet.
    """
    try:
        # Call the service to remove the medication
        medication_service.remove_medication(pet_id, medication_id)
        return {"message": "Medication deleted successfully"}
    except ValueError as e:
        # Handle not found case
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Handle generic errors
        raise HTTPException(status_code=500, detail="An error occurred while deleting the medication")