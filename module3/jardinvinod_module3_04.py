# Import FastAPI
from fastapi import FastAPI

# Import BaseModel for request data
from pydantic import BaseModel

# Import random to generate a random number
import random


# Create FastAPI application
app = FastAPI()


# Class to define person data
class Person(BaseModel):
    name: str
    phone_number: str


# Variable to store the last person received
saved_person = None


# POST API to save a person
@app.post("/person")
def create_person(person: Person):

    # Use global variable to store the person
    global saved_person

    saved_person = person

    # Return confirmation
    return {
        "message": "Person saved successfully",
        "name": person.name,
        "phone_number": person.phone_number
    }


# GET API to read the previous person
@app.get("/person")
def get_person():

    # Check if a person has been saved
    if saved_person is None:
        return {
            "message": "No person found"
        }

    # Generate a random number
    random_number = random.randint(1, 100)

    # Return the saved person with random number
    return {
        "name": saved_person.name,
        "phone_number": saved_person.phone_number,
        "random_number": random_number
    }