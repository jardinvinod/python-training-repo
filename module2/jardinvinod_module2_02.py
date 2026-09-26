# Function to encrypt a string
def encrypt_text(text):

    # Empty string to store the encrypted result
    encrypted_text = ""

    # Go through each character in the text
    for character in text:

        # Encrypt lowercase letters
        if "a" <= character <= "z":

            # Convert letter to a number, shift by 3,
            # then convert it back to a letter
            encrypted_character = chr(
                (ord(character) - ord("a") + 3) % 26 + ord("a")
            )

            encrypted_text += encrypted_character

        # Encrypt uppercase letters
        elif "A" <= character <= "Z":

            encrypted_character = chr(
                (ord(character) - ord("A") + 3) % 26 + ord("A")
            )

            encrypted_text += encrypted_character

        else:
            # Keep spaces, numbers and punctuation unchanged
            encrypted_text += character

    # Return the encrypted string
    return encrypted_text


# Get text from the user
user_text = input("Enter a string to encrypt: ")

# Encrypt the text
result = encrypt_text(user_text)

# Display the encrypted result
print("Encrypted text:", result)