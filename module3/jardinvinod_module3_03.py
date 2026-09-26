# Import FastAPI
from fastapi import FastAPI

# Import BaseModel to define the request body
from pydantic import BaseModel


# Create FastAPI application
app = FastAPI()


# Define the expected request body
class TextRequest(BaseModel):
    Text: str


# Create POST endpoint
@app.post("/check-text")
def check_text(data: TextRequest):

    # Return the received text
    return {
        "message": "Text received",
        "Text": data.Text
    }