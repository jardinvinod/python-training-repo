# Import sqlite3 to work with the SQLite database
import sqlite3

# Import time to wait for 15 seconds
import time


# Connect to the existing database
connection = sqlite3.connect("tasks.db")

# Create a cursor
cursor = connection.cursor()


# ID of the row that we want to modify
task_id = 1


# Read the existing row before changing it
cursor.execute(
    "SELECT title, description, status FROM tasks WHERE id = ?",
    (task_id,)
)

original_row = cursor.fetchone()


# Check if the row exists
if original_row is None:
    print("Task with ID", task_id, "does not exist.")

else:
    # Store the original values
    original_title = original_row[0]
    original_description = original_row[1]
    original_status = original_row[2]

    print("Original values:")
    print("Title:", original_title)
    print("Description:", original_description)
    print("Status:", original_status)


    # Change the values of the existing row
    cursor.execute("""
        UPDATE tasks
        SET title = ?,
            description = ?,
            status = ?
        WHERE id = ?
    """, (
        "Temporary Task",
        "This value will be reverted after 15 seconds",
        "Modified",
        task_id
    ))

    # Save the temporary change
    connection.commit()

    print("\nTask changed successfully.")
    print("The database will return to its original values after 15 seconds.")


    # Wait for 15 seconds
    time.sleep(15)


    # Restore the original values
    cursor.execute("""
        UPDATE tasks
        SET title = ?,
            description = ?,
            status = ?
        WHERE id = ?
    """, (
        original_title,
        original_description,
        original_status,
        task_id
    ))

    # Save the restored values
    connection.commit()

    print("\n15 seconds completed.")
    print("Original values restored successfully.")


# Close the database connection
connection.close()