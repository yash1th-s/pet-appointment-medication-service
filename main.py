from fastapi import FastAPI
from api import appointments, reminders, medications

app = FastAPI()


app.include_router(appointments.router, prefix="/appointment", tags=["appointments"])
app.include_router(medications.router, tags=["medications"])
app.include_router(reminders.router, prefix="/reminder", tags=["reminders"])
app.include_router(reminders.user_reminders_router, tags=["user-reminders"])


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Pet Management API"}