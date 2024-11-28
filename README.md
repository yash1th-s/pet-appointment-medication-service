
# Microservices for Appointment, Medication, and Reminders Management

This repository contains a set of microservices developed using **FastAPI** and **SAP HANA** to manage appointments, medications, and recurring reminders for pets.

## Table of Contents

1. [Overview](#overview)  
2. [Architecture](#architecture)  
3. [Features](#features)  
4. [Technologies Used](#technologies-used)  
5. [Installation](#installation)  
6. [Environment Variables](#environment-variables)  
7. [Usage](#usage)  
8. [Endpoints](#endpoints)  
9. [Deployment](#deployment)  
10. [Contributing](#contributing)  

---

## Overview

The microservices are designed to manage various aspects of pet care, including:
- Scheduling and managing appointments.
- Managing medication schedules.
- Handling recurring reminders for tasks like flea prevention.

---

## Architecture

The system is designed using the microservices architecture with the following components:
- **FastAPI** for the backend API.
- **SAP HANA** for the database.
- Optional support for **Docker** and **Nginx** for production deployment.

---

## Features

- CRUD operations for appointments, medications, and reminders.
- User-based filtering for reminders and appointments.
- Supports recurring reminders for regular tasks.

---

## Technologies Used

- **FastAPI** for API development.
- **Python** for backend logic.
- **SAP HANA** as the backend database.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/microservices.git
   cd microservices
   ```
2. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv env
   source env/bin/activate  # For Linux/macOS
   env\Scripts\activate     # For Windows
   pip install -r requirements.txt
   ```

---

## Environment Variables

Define environment variables in a `.env` file:
```env
ENV=development
DEBUG=True
DATABASE_HOST=DATABASE_HOST
DATABASE_PORT=DATABASE_PORT
DATABASE_USER=DATABASE_USER
DATABASE_PASSWORD=DATABASE_PASSWORD
DATABASE_NAME=DATABASE_NAME
```

---

## Usage

Run the application using:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
Access the Swagger UI at `http://localhost:8000/docs`.

---

## Endpoints

### Appointment Endpoints
- `POST /appointment/ - Create a new appointment.`
- `GET /appointment/{appointmentId} - Retrieve appointment by ID.`
- `PUT /appointment/{appointmentId} - Update an appointment.`
- `DELETE /appointment/{appointmentId} - Delete an appointment.`
- `GET /user/{userId}/appointments - Get all appointments for a user.`


### Medication Endpoints
- `POST /pet/{petId}/medication - Add a new medication schedule.`
- `GET /pet/{petId}/medications - Retrieve all medications for a pet.`
- `PUT /pet/{petId}/medication/{medicationId} - Update a medication schedule.`
- `DELETE /pet/{petId}/medication/{medicationId} - Delete a medication schedule.`

### Reminder Endpoints
- `POST /reminder - Create a recurring reminder.`
- `GET /reminder/{reminderId} - Retrieve a specific reminder.`
- `PUT /reminder/{reminderId} - Update a recurring reminder.`
- `DELETE /reminder/{reminderId} - Delete a reminder.`
- `GET /user/{userId}/reminders - Get all reminders for a user.`


---

## Deployment

Use Docker for deployment:
```bash
docker build -t microservices .
docker run -d -p 8000:8000 microservices
```

---

## Contact

For questions, contact:
- **Email**: yashwanths0210@gmail.com
- **GitHub**: [yash1th-s](https://github.com/yash1th-s)
