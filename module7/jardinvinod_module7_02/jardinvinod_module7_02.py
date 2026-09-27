# Import built-in modules
import json
import urllib.request
import os


# Get Ollama URL from environment variable
# Docker Compose will set this to http://ollama:11434
OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://ollama:11434"
)

# Ollama model name
MODEL_NAME = "qwen2.5:0.5b"


# Function to send user input to Ollama
def ask_ollama(user_text):

    # Ollama API endpoint
    url = f"{OLLAMA_URL}/api/generate"

    # Request data
    data = {
        "model": MODEL_NAME,
        "prompt": user_text,
        "stream": False
    }

    # Convert dictionary into JSON bytes
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

            # Read response
            response_data = response.read().decode("utf-8")

            # Convert JSON response into dictionary
            result = json.loads(response_data)

            # Return model response
            return result["response"]

    except Exception as error:
        return f"Error connecting to Ollama: {error}"


# Main program
while True:

    # Get input from user
    user_input = input(
        "\nEnter your question (or type 'exit'): "
    )

    # Exit program
    if user_input.lower() == "exit":
        print("Goodbye.")
        break

    # Ask Ollama
    result = ask_ollama(user_input)

    # Display response
    print("\nOllama Response:")
    print(result)