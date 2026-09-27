# Import FastAPI
from fastapi import FastAPI

# Import datetime for server time
from datetime import datetime

# Import platform and os for server information
import platform
import os


# Create FastAPI application
app = FastAPI()


# POST API for server health
@app.post("/health")
def server_health():

    # Get current server time
    server_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Return server health information
    return {
        "status": "healthy",
        "server_time": server_time,
        "hostname": platform.node(),
        "operating_system": platform.system(),
        "python_version": platform.python_version(),
        "process_id": os.getpid()
    }