# Function to accept only string values
def accept_string(value):
    try:
        # Check if the passed value is a string
        if not isinstance(value, str):
            raise TypeError

        # Return the string
        return value

    except TypeError:
        # Return NULL equivalent in Python
        return None


# Get input from the user
user_input = input("Enter a value: ")

# Try to convert the input to an integer
try:
    input_variable = int(user_input)

except ValueError:
    # Try to convert the input to a float
    try:
        input_variable = float(user_input)

    except ValueError:
        # If it is not a number, keep it as a string
        input_variable = user_input


# Pass the variable to the function
result = accept_string(input_variable)

# Display only the final result
print("Result:", result)