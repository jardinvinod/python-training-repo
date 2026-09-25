# Function to detect the correct data type of the user input
def convert_input(value):
    # Check for boolean values
    if value.lower() == "true":
        return True

    if value.lower() == "false":
        return False

    # Try to convert the value to an integer
    try:
        return int(value)
    except ValueError:
        pass

    # Try to convert the value to a float
    try:
        return float(value)
    except ValueError:
        pass

    # If no conversion works, keep it as a string
    return value


# Function to return variable content and data type
def print_variable(variable):
    # Get only the data type name, for example: int, float, str, bool
    data_type = type(variable).__name__

    # Create the required output format
    result = f"Result: (Variable content: {variable} , Data Type : '{data_type}' )"

    # Return the formatted result
    return result


# Take input from the user
user_input = input("Enter any value: ")

# Convert the input to the appropriate data type
converted_value = convert_input(user_input)

# Call the function and print the result
print(print_variable(converted_value))