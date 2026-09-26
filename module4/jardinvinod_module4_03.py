# Import FastAPI
from fastapi import FastAPI

# Import sqlite3 to work with SQLite database
import sqlite3


# Create FastAPI application
app = FastAPI()


# POST API to insert 2 rows into tasks table
@app.post("/tasks/add")
def add_tasks():

    # Connect to the existing SQLite database
    connection = sqlite3.connect("tasks.db")

    # Create cursor to execute SQL commands
    cursor = connection.cursor()

    # Insert first task
    cursor.execute("""
        INSERT INTO tasks (title, description, status)
        VALUES (?, ?, ?)
    """, (
        "Learn SQLite",
        "Practice inserting data into database",
        "Pending"
    ))

    # Insert second task
    cursor.execute("""
        INSERT INTO tasks (title, description, status)
        VALUES (?, ?, ?)
    """, (
        "Learn FastAPI",
        "Create POST API using FastAPI",
        "In Progress"
    ))

    # Save changes
    connection.commit()

    # Close database connection
    connection.close()

    # Return confirmation
    return {
        "message": "2 tasks inserted successfully"
    }