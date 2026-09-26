# Function to read the address file and add word count
def add_address_word_count():

    try:
        # Try to open and read the existing address book file
        with open("address_book.txt", "r") as file:
            lines = file.readlines()

        # List to store the updated file contents
        updated_lines = []

        # Index used to move through the lines
        i = 0

        while i < len(lines):

            # Get the current line
            line = lines[i]

            # Add the original line
            updated_lines.append(line)

            # Check if the current line contains an address
            if line.startswith("Address:"):

                # Remove "Address:" and get only the actual address
                address = line.replace("Address:", "").strip()

                # Count the words in the address
                word_count = len(address.split())

                # Check if Word Count already exists
                if i + 1 < len(lines) and lines[i + 1].startswith("Word Count:"):

                    # Replace the old word count
                    updated_lines.append(f"Word Count: {word_count}\n")

                    # Skip the existing Word Count line
                    i += 1

                else:
                    # Add a new Word Count line
                    updated_lines.append(f"Word Count: {word_count}\n")

            # Move to the next line
            i += 1

        # Write the updated content back into the same file
        with open("address_book.txt", "w") as file:
            file.writelines(updated_lines)

        print("Word count added successfully to address_book.txt")

    except FileNotFoundError:
        # Handle the case when the text file does not exist
        print("Error: address_book.txt file does not exist.")


# Call the function
add_address_word_count()