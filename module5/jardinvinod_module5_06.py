# Import Streamlit for the web interface
import streamlit as st

# Import built-in modules to call Ollama API
import json
import urllib.request


# Function to send the user's question to Ollama
def ask_ollama(user_text):

    # Ollama API endpoint
    url = "http://localhost:11434/api/generate"

    # Data sent to Ollama
    data = {
        "model": "qwen2.5:0.5b",
        "prompt": user_text,
        "stream": False
    }

    # Convert Python dictionary into JSON bytes
    json_data = json.dumps(data).encode("utf-8")

    # Create HTTP POST request
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

            # Read the API response
            response_data = response.read().decode("utf-8")

            # Convert JSON response into Python dictionary
            result = json.loads(response_data)

            # Return only the LLM answer
            return result["response"]

    except Exception as error:
        return f"Error: {error}"


# Streamlit page title
st.title("Local LLM Chat")

# Small description
st.write("Ask a question and get a response from Ollama.")


# Text box for user question
user_question = st.text_input(
    "Enter your question:"
)


# Button to send the question
if st.button("Ask LLM"):

    # Check that the user entered something
    if user_question.strip() == "":
        st.warning("Please enter a question.")

    else:
        # Display a loading message
        with st.spinner("LLM is thinking..."):

            # Send question to Ollama
            answer = ask_ollama(user_question)

        # Display result
        st.subheader("LLM Response")

        st.write(answer)