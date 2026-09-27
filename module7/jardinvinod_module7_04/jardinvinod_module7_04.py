# Import sqlite3 for database
import sqlite3

# Import random and string for random data
import random
import string


# Database file name
DATABASE_FILE = "users.db"


# Function to create random name
def random_name():
    names = [
        "Kevin",
        "Jardin",
        "Mohamed",
        "Sarah",
        "David",
        "Maria",
        "Ahmed",
        "John"
    ]

    return random.choice(names)


# Function to create random phone number
def random_phone():
    # Create a 10-digit phone number starting with 05
    remaining_digits = ""

    for i in range(8):
        remaining_digits += str(random.randint(0, 9))

    return "05" + remaining_digits


# Function to create random user key
def random_user_key():

    # Characters used for the key
    characters = string.ascii_uppercase + string.digits

    # Create an 8-character key
    user_key = ""

    for i in range(8):
        user_key += random.choice(characters)

    return user_key


# Function to create database and table
def create_database():

    # Connect to SQLite database
    connection = sqlite3.connect(DATABASE_FILE)

    # Create cursor
    cursor = connection.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            user_key TEXT NOT NULL
        )
    """)

    # Save changes
    connection.commit()

    # Close database
    connection.close()


# Function to insert random users
def insert_random_users(number_of_users):

    # Connect to database
    connection = sqlite3.connect(DATABASE_FILE)

    # Create cursor
    cursor = connection.cursor()

    # Insert random users
    for i in range(number_of_users):

        name = random_name()
        phone = random_phone()
        user_key = random_user_key()

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

    # Save changes
    connection.commit()

    # Close connection
    connection.close()


# Function to display stored users
def display_users():

    # Connect to database
    connection = sqlite3.connect(DATABASE_FILE)

    # Create cursor
    cursor = connection.cursor()

    # Read all users
    cursor.execute("""
        SELECT id, name, phone, user_key
        FROM users
    """)

    rows = cursor.fetchall()

    # Display data
    print("\nStored Users:")
    print("-" * 60)

    for row in rows:
        print(row)

    # Close connection
    connection.close()


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

# Create database and table
create_database()

# Insert 5 random users
insert_random_users(5)

# Display the data
display_users()