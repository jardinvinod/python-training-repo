# Import sqlite3 to work with SQLite database
import sqlite3


# Connect to the database
# If tasks.db does not exist, it will be created automatically
connection = sqlite3.connect("tasks.db")


# Create a cursor object to execute SQL commands
cursor = connection.cursor()


# Create tasks table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")


# Save the changes
connection.commit()


# Close the database connection
connection.close()


# Confirmation message
print("Database and tasks table created successfully.")