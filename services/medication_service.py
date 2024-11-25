from db.crud import add_medication_for_pet, get_medications_by_pet, update_medication, delete_medication
from models.medication import Medication, MedicationOut
from fastapi import HTTPException

def add_medication(medication: Medication):
    try:
        # Call CRUD function to add medication
        medication_id = add_medication_for_pet(medication)
        return medication_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add medication: {str(e)}")
    
    
def get_medications_for_pet(pet_id: int) -> list:
    medications = get_medications_by_pet(pet_id)
    if not medications:
        raise ValueError("No medications found for this pet")
    return medications


def update_medication_schedule(medication_id: int, medication_data: dict):
    """
    Updates a specific medication schedule using the CRUD function.
    """
    try:
        update_medication(medication_id, medication_data)
    except ValueError:
        raise ValueError("Medication not found")
    except Exception as e:
        raise Exception(f"An error occurred while updating the medication: {e}")
    

def remove_medication(pet_id: int, medication_id: int):
    """
    Service to delete a medication schedule.
    """
    try:
        delete_medication(pet_id, medication_id)
    except ValueError as e:
        # Handle case where medication is not found
        raise ValueError(str(e))
