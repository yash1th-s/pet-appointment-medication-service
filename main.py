from fastapi import FastAPI
from auth.auth_middleware import AuthMiddleware
from fastapi.security import HTTPBearer
from api import appointments, reminders, medications

app = FastAPI()


app.add_middleware(AuthMiddleware)

app.include_router(appointments.router, prefix="/appointment", tags=["appointments"])
app.include_router(medications.router, tags=["medications"])
app.include_router(reminders.router, prefix="/reminder", tags=["reminders"])
app.include_router(reminders.user_reminders_router, tags=["user-reminders"])


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Pet Management API"}


# Custom OpenAPI schema with JWT security
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = app.openapi_original()  # Generate the schema using FastAPI's original method
    openapi_schema["openapi"] = "3.0.3"  # Specify the OpenAPI version

    # Define security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Apply global security requirement
    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Store original OpenAPI method and override with the custom one
app.openapi_original = app.openapi
app.openapi = custom_openapi