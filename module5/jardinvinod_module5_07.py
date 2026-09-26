# Import Streamlit
import streamlit as st

# Import built-in modules to call Ollama API
import json
import urllib.request


# Function to send the full chat history to Ollama
def ask_ollama(messages):

    # Ollama chat API endpoint
    url = "http://localhost:11434/api/chat"

    # Data sent to Ollama
    data = {
        "model": "qwen2.5:0.5b",
        "messages": messages,
        "stream": False
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

            # Read the response
            response_data = response.read().decode("utf-8")

            # Convert JSON response to Python dictionary
            result = json.loads(response_data)

            # Return assistant response
            return result["message"]["content"]

    except Exception as error:
        return f"Error: {error}"


# Page title
st.title("Full LLM Chat")


# Create chat history if it does not already exist
if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. "
                "Remember the information given by the user "
                "during this conversation."
            )
        }
    ]


# Display previous chat messages
for message in st.session_state.messages:

    # Do not display the system prompt
    if message["role"] == "system":
        continue

    # Display user or assistant message
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Get new user message
user_input = st.chat_input("Enter your message")


# If the user enters a message
if user_input:

    # Add user message to chat history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)


    # Send the full conversation to Ollama
    with st.spinner("LLM is thinking..."):

        assistant_response = ask_ollama(
            st.session_state.messages
        )


    # Add assistant response to chat history
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response
        }
    )

    # Display assistant response
    with st.chat_message("assistant"):
        st.write(assistant_response)