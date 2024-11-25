from db.connection import get_db_connection
from datetime import datetime
from models.appointment import Appointment, AppointmentUpdate
from models.medication import Medication
from models.reminder import Reminder

  
def create_appointment(appointment: Appointment):
    """
    Creates a new appointment in the database.
    """
    # Get a connection to the HANA database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # SQL to insert the new appointment into the appointments table
    cursor.execute("""
        INSERT INTO PETSTORE.Appointments (pet_id, user_id, type, description, date_time, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        appointment.pet_id,
        appointment.user_id,
        appointment.type,
        appointment.description,
        appointment.date_time,
        appointment.status
    ))
    
    # Commit the transaction
    conn.commit()
    cursor.close()
    conn.close()

    
    
def get_appointment_by_id(appointment_id: int):
    """
    Retrieves an appointment by its ID from the database.
    """
    # Get a connection to the HANA database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # SQL to retrieve an appointment based on the ID
    cursor.execute("""
        SELECT id, pet_id, user_id, type, description, date_time, status
        FROM PETSTORE.Appointments
        WHERE id = ?
    """, (appointment_id,))
    
    # Fetch the result
    row = cursor.fetchone()
    
    # Close the connection
    cursor.close()
    conn.close()

    # If no appointment is found, raise an error or return None
    if row is None:
        return None

    # Return the appointment data as an Appointment object
    return Appointment(
        id=row[0],
        pet_id=row[1],
        user_id=row[2],
        type=row[3],
        description=row[4],
        date_time=row[5],
        status=row[6]
    )
    
    
    
    
def update_appointment(appointment_id: int, appointment: AppointmentUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build the SQL query dynamically based on the fields provided
    query = "UPDATE PETSTORE.Appointments SET "
    
    if appointment.type is not None:
        query += f"type = '{appointment.type}', "
    
    if appointment.description is not None:
        query += f"description = '{appointment.type}', "

    if appointment.date_time is not None:
        query += f"date_time = '{appointment.date_time}', "
    
    if appointment.status is not None:
        query += f"status = '{appointment.status}', "
    
    # Remove trailing comma and space from the query string
    query = query.rstrip(", ")

    query += f" WHERE id = {appointment_id}"
    
    
    
    # Execute the query
    cursor.execute(query)
    conn.commit()
    
    # Check if any rows were updated
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise ValueError("Appointment not found")
    
    cursor.close()
    conn.close()
    


def delete_appointment(appointment_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # SQL to delete the appointment from the appointments table
    cursor.execute("""
        DELETE FROM PETSTORE.Appointments
        WHERE id = ?
    """, (appointment_id,))
    
    conn.commit()
    
    # Check if the appointment was deleted (i.e., if any rows were affected)
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise ValueError("Appointment not found")
    
    cursor.close()
    conn.close()



def get_upcoming_appointments_by_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(f"""
        SELECT id, pet_id, type, date_time, description, status
        FROM PETSTORE.Appointments
        WHERE user_id = {user_id} AND date_time >= '{datetime.now()}'
        ORDER BY date_time ASC
    """)
    
    # Fetch all upcoming appointments
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # Convert the fetched rows into a list of Appointment models
    appointments = [
        {
            "appointment_id": row[0],
            "pet_id": row[1],
            "type": row[2],
            "date_time": row[3],
            "description": row[4],
            "status": row[5]
        }
        for row in rows
    ]

    return appointments


def get_appointments_by_pet(pet_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(f"""
        SELECT id, user_id, type, date_time, description, status
        FROM PETSTORE.Appointments
        WHERE pet_id = {pet_id} AND date_time >= '{datetime.now()}'
        ORDER BY date_time ASC
    """)
     
    # Fetch all upcoming appointments
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # Return the rows directly as a list of dictionaries
    appointments = [
        {
            "appointment_id": row[0],
            "user_id": row[1],
            "type": row[2],
            "date_time": row[3],
            "description": row[4],
            "status": row[5]
        }
        for row in rows
    ]

    return appointments



def add_medication_for_pet(medication: Medication) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL query to insert a new medication schedule into the database
    cursor.execute("""
        INSERT INTO PETSTORE.medications (pet_id, name, dosage, frequency, start_date, end_date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        medication.pet_id,
        medication.name,
        medication.dosage,
        medication.frequency,
        medication.start_date,
        medication.end_date,
        medication.notes
    ))

    # Commit the transaction and retrieve the inserted medication id
    conn.commit()
    
    cursor.execute(
    """
    SELECT MEDICATION_ID FROM PETSTORE.Medications
    WHERE PET_ID = ? AND NAME = ? AND START_DATE = ?
    ORDER BY MEDICATION_ID DESC
    LIMIT 1
    """,
    (medication.pet_id, medication.name, medication.start_date)
)

# Fetch the last inserted ID
    last_inserted_id = cursor.fetchone()[0]
    medication_id = last_inserted_id

    cursor.close()
    conn.close()
    return medication_id


def get_medications_by_pet(pet_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT MEDICATION_ID, pet_id, name, dosage, frequency, start_date, end_date, notes
        FROM PETSTORE.Medications
        WHERE pet_id = ?
    """, (pet_id,))
    
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # If no medications found, return an empty list
    if not rows:
        return []

    # Convert rows into list of dictionaries (or Medication models)
    medications = [
        {
            "id": row[0],
            "pet_id": row[1],
            "name": row[2],
            "dosage": row[3],
            "frequency": row[4],
            "start_date": row[5],
            "end_date": row[6],
            "notes": row[7]
        }
        for row in rows
    ]
    return medications


def update_medication(medication_id: int, medication_data: dict):
    """
    Updates a specific medication schedule in the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Dynamically build the update query based on provided fields
    fields_to_update = []
    for key, value in medication_data.items():
        fields_to_update.append(f"{key} = ?")
    
    update_query = f"""
        UPDATE PETSTORE.Medications
        SET {', '.join(fields_to_update)}
        WHERE MEDICATION_ID = ?
    """

    # Prepare parameters for the query
    parameters = list(medication_data.values())
    parameters.append(medication_id)

    # Execute the update query
    cursor.execute(update_query, parameters)
    conn.commit()

    # Check if any rows were affected
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise ValueError("Medication not found")

    cursor.close()
    conn.close()
    
    
    
def delete_medication(pet_id: int, medication_id: int):
    """
    Deletes a medication schedule for a pet.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # SQL to delete the medication
    cursor.execute("""
        DELETE FROM PETSTORE.Medications
        WHERE MEDICATION_ID = ? AND pet_id = ?
    """, (medication_id, pet_id))
    
    # Commit the transaction
    conn.commit()

    # Check if a row was deleted
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise ValueError("Medication not found")
    
    # Clean up
    cursor.close()
    conn.close()
    
    
def create_reminder(reminder: Reminder):
    """
    Inserts a new reminder into the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # SQL to insert the new reminder
    insert_query = """
        INSERT INTO PETSTORE.Reminders (user_id, title, description, frequency, start_date, end_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    
    cursor.execute(insert_query, (
        reminder.user_id,
        reminder.title,
        reminder.description,
        reminder.frequency,
        reminder.start_date,
        reminder.end_date,
        reminder.status
    ))
    
    # Commit the transaction and get the inserted ID
    conn.commit()
    cursor.execute(
    """
    SELECT REMINDER_ID FROM PETSTORE.Reminders
    WHERE USER_ID = ? AND TITLE = ? AND START_DATE = ?
    ORDER BY REMINDER_ID DESC
    LIMIT 1
    """,
    (reminder.user_id, reminder.title, reminder.start_date)
)

# Fetch the last inserted ID
    last_inserted_id = cursor.fetchone()[0]
    reminder_id = last_inserted_id

    cursor.close()
    conn.close()
    return reminder_id



def get_reminder_by_id(reminder_id: int):
    """
    Retrieves a reminder by its ID from the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # SQL query to fetch the reminder
    query = """
        SELECT reminder_id, user_id, title, description, frequency, start_date, end_date, status
        FROM PETSTORE.Reminders
        WHERE reminder_id = ?
    """
    
    cursor.execute(query, (reminder_id,))
    row = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if row is None:
        return None
    
    # Return the row as a dictionary
    return {
        "reminder_id": row[0],
        "user_id": row[1],
        "title": row[2],
        "description": row[3],
        "frequency": row[4],
        "start_date": row[5],
        "end_date": row[6],
        "status": row[7]
    }
