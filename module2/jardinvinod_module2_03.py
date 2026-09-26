# Function to find unique numbers from a list
def find_unique_numbers(numbers):

    # Empty list to store unique numbers
    unique_numbers = []

    # Go through each number in the list
    for number in numbers:

        # Add the number only if it is not already in the unique list
        if number not in unique_numbers:
            unique_numbers.append(number)

    # Return the unique list
    return unique_numbers


# Get numbers from the user
user_input = input("Enter numbers separated by spaces: ")

# Convert the input into a list of integers
numbers = [int(number) for number in user_input.split()]

# Call the function
result = find_unique_numbers(numbers)

# Display the result
print("Unique numbers:", result)