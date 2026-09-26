# Import sqlite3
import sqlite3


# Connect to the existing database
connection = sqlite3.connect("tasks.db")

# Create cursor
cursor = connection.cursor()


# Read all rows from the table
cursor.execute("SELECT * FROM tasks")

rows = cursor.fetchall()


# Sort rows in Python
# missing_field is the last column, so index -1 is used
sorted_rows = sorted(
    rows,
    key=lambda row: row[-1]
)


# Display sorted data
print("Tasks ordered by missing_field using Python:")

for row in sorted_rows:
    print(row)


# Close database connection
connection.close()