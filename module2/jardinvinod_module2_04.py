# Import json module to work with JSON files
import json


# Class to store information about a person
class Person:

    # Constructor to initialize person details
    def __init__(self, name, number, location, job_title):
        self.name = name
        self.number = number
        self.location = location
        self.job_title = job_title

    # Function to convert the object into dictionary format
    def to_dictionary(self):
        return {
            "name": self.name,
            "number": self.number,
            "location": self.location,
            "job_title": self.job_title
        }


# Function to save people into a JSON file
def save_people_to_json(people):

    # Convert all Person objects into dictionaries
    people_list = []

    for person in people:
        people_list.append(person.to_dictionary())

    # Open the JSON file in write mode
    with open("people.json", "w") as file:

        # Save the list into the JSON file
        json.dump(people_list, file, indent=4)

    # Display confirmation
    print("People information saved successfully in people.json")


# Create 5 sample people
person1 = Person("John Smith", 101, "London", "Engineer")
person2 = Person("Maria Lopez", 102, "Madrid", "Doctor")
person3 = Person("David Martin", 103, "Paris", "Teacher")
person4 = Person("Sarah Wilson", 104, "New York", "Designer")
person5 = Person("Ahmed Ali", 105, "Dubai", "Manager")


# Store all people in a list
people = [
    person1,
    person2,
    person3,
    person4,
    person5
]


# Call the function to save the people into JSON
save_people_to_json(people)