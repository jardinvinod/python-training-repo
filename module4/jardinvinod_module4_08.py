# Import sqlite3
import sqlite3


# Function to search only the description column
def search_description(search_value):

    # Connect to the existing database
    connection = sqlite3.connect("tasks.db")

    # Create cursor
    cursor = connection.cursor()

    # Add % before and after the search value
    # This allows partial matching
    search_pattern = f"%{search_value}%"

    # Search only inside the description column
    cursor.execute("""
        SELECT *
        FROM tasks
        WHERE description LIKE ?
    """, (search_pattern,))

    # Get all matching rows
    rows = cursor.fetchall()

    # Close the database connection
    connection.close()

    # Return matching rows
    return rows


# Get search input from the user
search_value = input("Enter letters or number to search in description: ")

# Call the search function
results = search_description(search_value)


# Display the results
if len(results) == 0:
    print("No matching rows found.")

else:
    print("\nMatching rows:")

    for row in results:
        print(row)