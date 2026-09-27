# Import sqlite3 for database
import sqlite3

# Import os to check database location
import os


# Database is stored outside the container
DATABASE_FILE = "/data/users.db"


# Function to create database/table if they do not exist
def create_database():

    # Connect to the existing database
    # If it does not exist, SQLite will create it
    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    # CREATE TABLE IF NOT EXISTS protects the existing table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            user_key TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# Function to add a new user
def add_user(name, phone, user_key):

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    # INSERT adds a new row without deleting old rows
    cursor.execute("""
        INSERT INTO users (
            name,
            phone,
            user_key
        )
        VALUES (?, ?, ?)
    """, (
        name,
        phone,
        user_key
    ))

    connection.commit()
    connection.close()


# Function to display all existing users
def display_users():

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, phone, user_key
        FROM users
        ORDER BY id
    """)

    rows = cursor.fetchall()

    print("\nStored Users:")
    print("-" * 60)

    if len(rows) == 0:
        print("No users found.")

    else:
        for row in rows:
            print(row)

    connection.close()


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

# Create table only if needed
create_database()

# Show old database records first
display_users()


# Get information from user
print("\nAdd New User")

name = input("Enter name: ")
phone = input("Enter phone number: ")
user_key = input("Enter user key: ")


# Add new information
add_user(
    name,
    phone,
    user_key
)

print("\nUser added successfully.")


# Show old + new records
display_users()