from fastapi import FastAPI
from api import appointments, reminders, medications

app = FastAPI()


app.include_router(appointments.router, prefix="/appointment", tags=["appointments"])
