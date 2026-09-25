# Class to store the address details of a person
class PersonAddress:

    # Constructor to initialize the person's details
    def __init__(self, name, contact, address, phone_number):
        self.name = name
        self.contact = contact
        self.address = address
        self.phone_number = phone_number

    # Function to save the person's details into a text file
    def save_to_file(self):

        # Open the text file in append mode
        # "a" means new records will be added without deleting old records
        with open("address_book.txt", "a") as file:

            # Write the person's information into the file
            file.write("Name: " + self.name + "\n")
            file.write("Contact: " + self.contact + "\n")
            file.write("Address: " + self.address + "\n")
            file.write("Phone Number: " + self.phone_number + "\n")

            # Add a separator between different people
            file.write("------------------------------\n")


# Take input from the user
name = input("Enter name: ")
contact = input("Enter contact: ")
address = input("Enter address: ")
phone_number = input("Enter phone number: ")

# Create an object of the PersonAddress class
person = PersonAddress(name, contact, address, phone_number)

# Save the information into the text file
person.save_to_file()

# Display confirmation message
print("Address saved successfully in address_book.txt")