# Import Streamlit for the user interface
import streamlit as st

# Import SQLite for database storage
import sqlite3

# Import Pydantic for structured validation
from pydantic import BaseModel, model_validator, field_validator

# Built-in modules for Ollama API
import json
import urllib.request

# Import regular expressions for phone number fallback
import re


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

DATABASE_FILE = "structured_data.db"
OLLAMA_MODEL = "qwen2.5:0.5b"


# --------------------------------------------------
# PYDANTIC MODEL
# --------------------------------------------------

class UserInformation(BaseModel):

    # All fields are optional individually
    name: str | None = None
    time: str | None = None
    number: str | None = None


    # Convert empty or placeholder values into None
    @field_validator("name", "time", "number", mode="before")
    @classmethod
    def clean_empty_values(cls, value):

        # If value is already None
        if value is None:
            return None

        # Convert value to string and remove spaces
        cleaned_value = str(value).strip()

        # Placeholder values that should become NULL
        null_values = [
            "",
            "null",
            "none",
            "n/a",
            "unknown",
            "not available",
            "0000000000"
        ]

        # Convert placeholder values to None
        if cleaned_value.lower() in null_values:
            return None

        return cleaned_value


    # At least one field must contain real information
    @model_validator(mode="after")
    def check_at_least_one_value(self):

        if not self.name and not self.time and not self.number:
            raise ValueError(
                "At least one of name, time or number is required."
            )

        return self


# --------------------------------------------------
# CREATE DATABASE
# --------------------------------------------------

def create_database():

    # Connect to SQLite database
    connection = sqlite3.connect(DATABASE_FILE)

    # Create cursor
    cursor = connection.cursor()

    # Create table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_information (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            time TEXT,
            number TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Save changes
    connection.commit()

    # Close connection
    connection.close()


# --------------------------------------------------
# SAVE DATA INTO DATABASE
# --------------------------------------------------

def save_to_database(data):

    # Connect to SQLite database
    connection = sqlite3.connect(DATABASE_FILE)

    # Create cursor
    cursor = connection.cursor()

    # Insert structured data
    cursor.execute("""
        INSERT INTO user_information (
            name,
            time,
            number
        )
        VALUES (?, ?, ?)
    """, (
        data.name,
        data.time,
        data.number
    ))

    # Save changes
    connection.commit()

    # Close connection
    connection.close()


# --------------------------------------------------
# READ DATABASE
# --------------------------------------------------

def read_database():

    # Connect to SQLite database
    connection = sqlite3.connect(DATABASE_FILE)

    # Create cursor
    cursor = connection.cursor()

    # Read all stored rows
    cursor.execute("""
        SELECT id, name, time, number, created_at
        FROM user_information
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    # Close connection
    connection.close()

    return rows


# --------------------------------------------------
# EXTRACT INFORMATION USING OLLAMA
# --------------------------------------------------

def extract_information(user_text):

    # Ollama API endpoint
    url = "http://localhost:11434/api/generate"

    # Prompt for structured extraction
    prompt = f"""
Extract ONLY these fields from the user text:

- name
- time
- number

Rules:

1. "number" means phone number or numeric contact number.
2. Keep phone numbers exactly as written.
3. Do not remove leading zeroes.
4. If a value is not present, return null.
5. Do NOT invent placeholder values.
6. Do NOT use 0000000000 for missing numbers.
7. Do NOT use an empty string for missing values.
8. Return ONLY valid JSON.
9. Do not include explanations.

Required JSON format:

{{
    "name": null,
    "time": null,
    "number": null
}}

Example 1:

User text:
My name is Jardin, call me at 0501234567 at 10:30 AM.

Correct JSON:

{{
    "name": "Jardin",
    "time": "10:30 AM",
    "number": "0501234567"
}}

Example 2:

User text:
My name is Kevin.

Correct JSON:

{{
    "name": "Kevin",
    "time": null,
    "number": null
}}

Now extract information from:

{user_text}
"""

    # Data sent to Ollama
    data = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    # Convert dictionary to JSON bytes
    json_data = json.dumps(data).encode("utf-8")

    # Create POST request
    request = urllib.request.Request(
        url,
        data=json_data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:

        # Send request to Ollama
        with urllib.request.urlopen(request) as response:

            # Read API response
            response_data = response.read().decode("utf-8")

            # Convert Ollama response into dictionary
            ollama_result = json.loads(response_data)

            # Get generated JSON text
            generated_text = ollama_result["response"]

            # Convert generated JSON into Python dictionary
            extracted_data = json.loads(generated_text)


            # --------------------------------------------------
            # PHONE NUMBER FALLBACK
            # --------------------------------------------------

            # Get the number returned by the LLM
            current_number = extracted_data.get("number")

            # Treat placeholder values as missing
            if current_number is not None:
                current_number_text = str(current_number).strip().lower()

                if current_number_text in [
                    "",
                    "null",
                    "none",
                    "n/a",
                    "unknown",
                    "0000000000"
                ]:
                    current_number = None


            # If number is missing, look for a real phone number
            if current_number is None:

                phone_match = re.search(
                    r"\b\d{7,15}\b",
                    user_text
                )

                if phone_match:
                    extracted_data["number"] = phone_match.group()

                else:
                    extracted_data["number"] = None


            return extracted_data


    except Exception as error:

        st.error(f"LLM Error: {error}")

        return None


# --------------------------------------------------
# INITIALIZE DATABASE
# --------------------------------------------------

create_database()


# --------------------------------------------------
# STREAMLIT UI
# --------------------------------------------------

st.title("LLM Structured Data")

st.write(
    "Enter information containing a name, time, number, "
    "or any combination of them."
)


# User input
user_input = st.text_area(
    "Enter your information:"
)


# Process button
if st.button("Process Information"):

    # Check for empty input
    if user_input.strip() == "":

        st.warning("Please enter some information.")

    else:

        # Ask Ollama to extract structured information
        with st.spinner("LLM is extracting information..."):

            extracted_data = extract_information(
                user_input
            )


        # Continue only if extraction succeeded
        if extracted_data is not None:

            try:

                # ------------------------------------------
                # VALIDATE USING PYDANTIC
                # ------------------------------------------

                structured_data = UserInformation(
                    **extracted_data
                )


                # Display Pydantic result
                st.subheader("Pydantic Result")

                st.json(
                    structured_data.model_dump()
                )


                # ------------------------------------------
                # SAVE INTO SQLITE DATABASE
                # ------------------------------------------

                save_to_database(
                    structured_data
                )

                st.success(
                    "Information saved successfully "
                    "in SQL database."
                )


            except Exception as error:

                st.error(
                    f"Validation Error: {error}"
                )


# --------------------------------------------------
# DISPLAY STORED DATABASE INFORMATION
# --------------------------------------------------

st.subheader("Stored Information")

rows = read_database()


if len(rows) == 0:

    st.write("No information stored yet.")

else:

    for row in rows:

        st.write({
            "id": row[0],
            "name": row[1],
            "time": row[2],
            "number": row[3],
            "created_at": row[4]
        })