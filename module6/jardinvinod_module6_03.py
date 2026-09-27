# Import Streamlit for UI
import streamlit as st

# Import sqlite3 for SQL database
import sqlite3

# Import built-in modules to call Ollama API
import json
import urllib.request


# --------------------------------------------------
# DATABASE SETTINGS
# --------------------------------------------------

DATABASE_FILE = "chat_history.db"


# Function to create the database table
def create_database():

    # Connect to SQLite database
    connection = sqlite3.connect(DATABASE_FILE)

    # Create cursor
    cursor = connection.cursor()

    # Create chat_history table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_question TEXT NOT NULL,
            llm_response TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Save changes
    connection.commit()

    # Close connection
    connection.close()


# Function to save chat into database
def save_chat(user_question, llm_response):

    # Connect to database
    connection = sqlite3.connect(DATABASE_FILE)

    # Create cursor
    cursor = connection.cursor()

    # Insert chat information
    cursor.execute("""
        INSERT INTO chat_history (
            user_question,
            llm_response
        )
        VALUES (?, ?)
    """, (
        user_question,
        llm_response
    ))

    # Save changes
    connection.commit()

    # Close database connection
    connection.close()


# Function to call Ollama API
def ask_ollama(user_text):

    # Ollama API URL
    url = "http://localhost:11434/api/generate"

    # Data sent to Ollama
    data = {
        "model": "qwen2.5:0.5b",
        "prompt": user_text,
        "stream": False
    }

    # Convert dictionary to JSON bytes
    json_data = json.dumps(data).encode("utf-8")

    # Create HTTP request
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

            # Read response
            response_data = response.read().decode("utf-8")

            # Convert JSON response to dictionary
            result = json.loads(response_data)

            # Return LLM answer
            return result["response"]

    except Exception as error:

        return f"Error: {error}"


# --------------------------------------------------
# START DATABASE
# --------------------------------------------------

create_database()


# --------------------------------------------------
# STREAMLIT UI
# --------------------------------------------------

st.title("LLM Chat with SQL Database")

st.write(
    "Ask a question. The question and LLM response "
    "will be stored in SQLite."
)


# Input box
user_question = st.text_input(
    "Enter your question:"
)


# Ask button
if st.button("Ask LLM"):

    # Check if input is empty
    if user_question.strip() == "":

        st.warning("Please enter a question.")

    else:

        # Call the LLM
        with st.spinner("LLM is thinking..."):

            answer = ask_ollama(user_question)

        # Display result
        st.subheader("LLM Response")

        st.write(answer)

        # Store question and answer in database
        save_chat(
            user_question,
            answer
        )

        # Confirmation
        st.success(
            "Chat saved successfully in SQL database."
        )