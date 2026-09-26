# Import sqlite3
import sqlite3


# Connect to the existing database
connection = sqlite3.connect("tasks.db")

# Create cursor
cursor = connection.cursor()


# Select all rows ordered by missing_field
cursor.execute("""
    SELECT *
    FROM tasks
    ORDER BY missing_field ASC
""")


# Fetch the ordered rows
rows = cursor.fetchall()


# Display the ordered data
print("Tasks ordered by missing_field using SQL:")

for row in rows:
    print(row)


# Close the connection
connection.close()