# Import FastAPI
from fastapi import FastAPI

# Import BaseModel to define the POST request body
from pydantic import BaseModel

# Import datetime to get the server time
from datetime import datetime


# Create FastAPI application
app = FastAPI()


# Create a class for the incoming message
class Message(BaseModel):
    message: str


# Create POST API endpoint
@app.post("/echo")
def echo_message(data: Message):

    # Get the current server date and time
    server_time = datetime.now()

    # Format the server timestamp
    timestamp = server_time.strftime("%Y-%m-%d %H:%M:%S")

    # Return the message with server timestamp
    return {
        "message": data.message,
        "server_timestamp": timestamp
    }