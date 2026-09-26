# Import sqlite3
import sqlite3


# Connect to database
connection = sqlite3.connect("tasks.db")

# Create cursor
cursor = connection.cursor()


# Get all user-created tables
cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    AND name NOT LIKE 'sqlite_%'
""")

tables = cursor.fetchall()


# Go through every table
for table in tables:

    table_name = table[0]

    print("\nTable:", table_name)
    print("-" * 70)

    # Get table column information
    cursor.execute(f"PRAGMA table_info({table_name})")

    columns = cursor.fetchall()

    # Display column names
    column_names = []

    for column in columns:
        column_names.append(column[1])

    print("Columns:", column_names)


    # Read all data from the table
    cursor.execute(f"SELECT * FROM {table_name}")

    rows = cursor.fetchall()

    # Display rows
    if len(rows) == 0:
        print("No data found.")

    else:
        for row in rows:
            print(row)


# Close database connection
connection.close()