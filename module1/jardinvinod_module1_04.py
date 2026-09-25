# Import datetime to get the current date and time
from datetime import datetime


# Function to return current date and time
def get_current_date_time(current_time):
    # Format: seconds:minutes:hours , day/month/year
    return current_time.strftime("%S:%M:%H , %d/%m/%Y")


# Function to generate Fibonacci sequence
def generate_fibonacci(number_of_terms):
    # Starting values of Fibonacci sequence
    first = 0
    second = 1

    # Empty list to store the sequence
    sequence = []

    # Generate Fibonacci numbers
    for i in range(number_of_terms):
        # Store the current number
        sequence.append(first)

        # Calculate the next number
        first, second = second, first + second

    # Return the complete sequence
    return sequence


# Get the current date and time once
now = datetime.now()

# Get the current minute
current_minute = now.minute

# Number of Fibonacci terms = 2 * current minute
number_of_terms = 2 * current_minute

# Generate Fibonacci sequence
fibonacci_sequence = generate_fibonacci(number_of_terms)

# Display the results
print("Current Date and Time:", get_current_date_time(now))
print("Current Minute:", current_minute)
print("Number of Fibonacci Terms:", number_of_terms)
print("Fibonacci Sequence:", fibonacci_sequence)