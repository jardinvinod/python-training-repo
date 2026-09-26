# Import Streamlit
import streamlit as st

# Import built-in modules
import json
import urllib.request
import os


# File used to store chat history
CHAT_FILE = "chat_history.json"


# Function to load previous chat history
def load_chat_history():

    # Check if chat file already exists
    if os.path.exists(CHAT_FILE):

        try:
            # Open and read the JSON file
            with open(CHAT_FILE, "r", encoding="utf-8") as file:
                return json.load(file)

        except Exception:
            # If file cannot be read, start with empty history
            return []

    # If file does not exist, return empty list
    return []


# Function to save chat history
def save_chat_history(messages):

    # Write all messages into JSON file
    with open(CHAT_FILE, "w", encoding="utf-8") as file:

        json.dump(
            messages,
            file,
            indent=4,
            ensure_ascii=False
        )


# Function to send full chat history to Ollama
def ask_ollama(messages):

    # Ollama API endpoint
    url = "http://localhost:11434/api/chat"

    # Data sent to Ollama
    data = {
        "model": "qwen2.5:0.5b",
        "messages": messages,
        "stream": False
    }

    # Convert Python dictionary to JSON bytes
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

            # Read response
            response_data = response.read().decode("utf-8")

            # Convert JSON response to dictionary
            result = json.loads(response_data)

            # Return assistant answer
            return result["message"]["content"]

    except Exception as error:
        return f"Error: {error}"


# Page title
st.title("Persistent LLM Chat")


# Load previous messages only once when app starts
if "messages" not in st.session_state:

    st.session_state.messages = load_chat_history()

    # If there is no previous history, add system prompt
    if len(st.session_state.messages) == 0:

        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. "
                    "Remember information from the user's previous messages."
                )
            }
        ]


# Display previous chat messages
for message in st.session_state.messages:

    # Do not display system prompt
    if message["role"] == "system":
        continue

    # Display user and assistant messages
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Get new user message
user_input = st.chat_input("Enter your message")


# If user sends a message
if user_input:

    # Add user message to chat history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Save immediately
    save_chat_history(st.session_state.messages)

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)


    # Send full conversation to Ollama
    with st.spinner("LLM is thinking..."):

        assistant_response = ask_ollama(
            st.session_state.messages
        )


    # Add assistant response to history
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response
        }
    )

    # Save updated conversation
    save_chat_history(st.session_state.messages)


    # Display assistant response
    with st.chat_message("assistant"):
        st.write(assistant_response)


# Button to clear stored history
if st.button("Clear Chat History"):

    # Reset session history
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. "
                "Remember information from the user's previous messages."
            )
        }
    ]

    # Save cleared history
    save_chat_history(st.session_state.messages)

    # Refresh UI
    st.rerun()