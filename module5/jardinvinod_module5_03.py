# Import built-in modules
import json
import urllib.request


# Function to send prompt to Ollama API
def ask_ollama(user_text):

    # Ollama API URL
    url = "http://localhost:11434/api/generate"

    # Data to send to Ollama
    data = {
        "model": "qwen2.5:0.5b",
        "prompt": user_text,
        "stream": False
    }

    # Convert Python dictionary to JSON bytes
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

            # Read the response
            response_data = response.read().decode("utf-8")

            # Convert JSON response to Python dictionary
            result = json.loads(response_data)

            # Return only the generated response text
            return result["response"]

    except Exception as error:

        # Return error message if API call fails
        return f"Error: {error}"


# Get input from the user
user_input = input("Enter your prompt: ")

# Send input to Ollama
result = ask_ollama(user_input)

# Display the result
print("\nOllama response:")
print(result)