from db.crud import create_appointment, get_appointment_by_id, update_appointment, delete_appointment, get_upcoming_appointments_by_user, get_appointments_by_pet
from models.appointment import Appointment, AppointmentUpdate

def schedule_appointment(user_id: str, appointment: Appointment):    
    create_appointment(user_id, appointment)
    
def get_appointment_details(appointment_id: int) -> Appointment:
    # Retrieve the appointment details from the database
    appointment = get_appointment_by_id(appointment_id)
    if not appointment:
        raise ValueError("Appointment not found")
    return appointment

def update_appointment_details(appointment_id: int, appointment: AppointmentUpdate):
    try:
        update_appointment(appointment_id, appointment)
    except ValueError:
        raise ValueError("Appointment not found")
    
    
def cancel_appointment(appointment_id: int):
    try:
        # Call the CRUD function to delete the appointment
        delete_appointment(appointment_id)
    except ValueError:
        # Raise an error if the appointment doesn't exist
        raise ValueError("Appointment not found")
    

def get_upcoming_appointments(user_id: str) -> list[Appointment]:
    # Retrieve upcoming appointments from the database
    appointments = get_upcoming_appointments_by_user(user_id)
    
    if not appointments:
        raise ValueError("No upcoming appointments found for this user")
    return appointments


def get_appointments_for_pet(pet_id: str) -> list[dict]:
    # Retrieve upcoming appointments for the pet
    appointments = get_appointments_by_pet(pet_id)
    if not appointments:
        raise ValueError("No upcoming appointments found for this pet")
    return appointments