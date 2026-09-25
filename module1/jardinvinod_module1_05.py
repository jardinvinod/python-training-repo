# Function to shift letters and calculate word count and price
def speaking_is_expensive(text, price_per_letter):

    # Empty string to store the shifted text
    shifted_text = ""

    # Counter to count only letters
    letter_count = 0

    # Go through each character in the text
    for character in text:

        # Check if the character is a lowercase letter
        if "a" <= character <= "z":

            # If the letter is z, shift it back to a
            if character == "z":
                shifted_text += "a"
            else:
                # Shift the letter by one position
                shifted_text += chr(ord(character) + 1)

            # Increase letter count
            letter_count += 1

        # Check if the character is an uppercase letter
        elif "A" <= character <= "Z":

            # If the letter is Z, shift it back to A
            if character == "Z":
                shifted_text += "A"
            else:
                # Shift the letter by one position
                shifted_text += chr(ord(character) + 1)

            # Increase letter count
            letter_count += 1

        else:
            # Keep spaces, numbers and punctuation unchanged
            shifted_text += character

    # Count the number of words
    word_count = len(text.split())

    # Calculate total price
    total_price = letter_count * price_per_letter

    # Store the results in dictionary format
    result = {
        "Shifted String": shifted_text,
        "Word Count": word_count,
        "String Price": total_price
    }

    # Return the dictionary
    return result


# Take text input from the user
user_text = input("Enter a sentence: ")

# Take price per letter from the user
price = float(input("Enter price per letter: "))

# Call the function
result = speaking_is_expensive(user_text, price)

# Display the result
print("Result:", result)