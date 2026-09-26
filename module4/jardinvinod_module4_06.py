# Import sqlite3 to work with SQLite database
import sqlite3


# Connect to the existing database
connection = sqlite3.connect("tasks.db")

# Create cursor
cursor = connection.cursor()


# Check if missing_field already exists
cursor.execute("PRAGMA table_info(tasks)")

columns = cursor.fetchall()

column_names = []

for column in columns:
    column_names.append(column[1])


# Add the new column only if it does not already exist
if "missing_field" not in column_names:

    cursor.execute("""
        ALTER TABLE tasks
        ADD COLUMN missing_field TEXT
    """)

    print("Column 'missing_field' added successfully.")

else:

    print("Column 'missing_field' already exists.")


# Populate missing_field with one random uppercase character
cursor.execute("""
    UPDATE tasks
    SET missing_field =
        substr(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            (abs(random()) % 26) + 1,
            1
        )
""")


# Save the changes
connection.commit()


# Display the updated table
cursor.execute("SELECT * FROM tasks")

rows = cursor.fetchall()


print("\nUpdated tasks table:")

for row in rows:
    print(row)


# Close database connection
connection.close()