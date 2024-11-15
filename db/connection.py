from hdbcli import dbapi
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    conn = dbapi.connect(
        address = os.getenv("DATABASE_HOST"),
        port = os.getenv("DATABASE_PORT"),
        user = os.getenv("DATABASE_USER"),
        password = os.getenv("DATABASE_PASSWORD"),
        encrypt=True
    )
    return conn
