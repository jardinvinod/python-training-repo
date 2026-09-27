# Import Streamlit for the UI
import streamlit as st

# Built-in modules for Ollama API
import json
import urllib.request
import os


# --------------------------------------------------
# ENVIRONMENT VARIABLES
# --------------------------------------------------

# Ollama URL supplied by Docker Compose
OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://ollama:11434"
)

# Ollama model
OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen2.5:0.5b"
)

# Environment variable used to enable/disable persona
USE_PERSONA = os.getenv(
    "USE_PERSONA",
    "false"
).lower() == "true"


# --------------------------------------------------
# PERSONA
# --------------------------------------------------

PERSONA_PROMPT = (
    "You are a friendly Python programming teacher. "
    "Explain answers clearly using simple language and "
    "small examples."
)


# --------------------------------------------------
# FUNCTION TO CALL OLLAMA
# --------------------------------------------------

def ask_ollama(messages):

    # Ollama chat API
    url = f"{OLLAMA_URL}/api/chat"

    # Data sent to Ollama
    data = {
        "model": OLLAMA_MODEL,
        "messages": messages,
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

        # Send request
        with urllib.request.urlopen(request) as response:

            response_data = response.read().decode("utf-8")

            result = json.loads(response_data)

            return result["message"]["content"]

    except Exception as error:

        return f"Error connecting to Ollama: {error}"


# --------------------------------------------------
# STREAMLIT PAGE
# --------------------------------------------------

st.title("Docker Ollama Chat")


# Show current mode
if USE_PERSONA:

    st.success("Persona Mode: ON")

    st.write(
        "The assistant is acting as a friendly Python teacher."
    )

else:

    st.info("Persona Mode: OFF")


# --------------------------------------------------
# CHAT MEMORY
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# --------------------------------------------------
# GET USER MESSAGE
# --------------------------------------------------

user_input = st.chat_input(
    "Enter your message"
)


if user_input:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Display user message
    with st.chat_message("user"):

        st.write(user_input)


    # --------------------------------------------------
    # CREATE MESSAGES FOR OLLAMA
    # --------------------------------------------------

    ollama_messages = []

    # Add system persona only if environment variable is enabled
    if USE_PERSONA:

        ollama_messages.append(
            {
                "role": "system",
                "content": PERSONA_PROMPT
            }
        )


    # Add conversation history
    ollama_messages.extend(
        st.session_state.messages
    )


    # --------------------------------------------------
    # ASK OLLAMA
    # --------------------------------------------------

    with st.spinner("LLM is thinking..."):

        answer = ask_ollama(
            ollama_messages
        )


    # Save assistant answer
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    # Display answer
    with st.chat_message("assistant"):

        st.write(answer)