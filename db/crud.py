from db.connection import get_db_connection
from datetime import datetime
from models.appointment import Appointment, AppointmentUpdate

  
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