# Function to check if a number is even or odd
def check_even_odd(number):

    # If the remainder after division by 2 is 0,
    # the number is even
    if number % 2 == 0:
        return "Even Number"

    # Otherwise, the number is odd
    else:
        return "Odd Number"


# Get a number from the user
number = int(input("Enter a number: "))

# Call the function and store the result
result = check_even_odd(number)

# Display the result
print("Result:", result)