# Import built-in modules
import json
import urllib.request


# Function to ask Ollama with custom context window and temperature
def ask_ollama(user_text):

    # Ollama API endpoint
    url = "http://localhost:11434/api/generate"

    # Data sent to Ollama
    data = {
        "model": "qwen2.5:0.5b",
        "prompt": user_text,
        "stream": False,

        # Options used by the model
        "options": {
            # Increase the context window
            "num_ctx": 4096,

            # Control randomness of the answer
            "temperature": 0.7
        }
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

            # Read response
            response_data = response.read().decode("utf-8")

            # Convert JSON response into Python dictionary
            result = json.loads(response_data)

            # Return model answer
            return result["response"]

    except Exception as error:
        return f"Error: {error}"


# Take input from the user
user_input = input("Enter your prompt: ")

# Send prompt to Ollama
result = ask_ollama(user_input)

# Display the result
print("\nLLM Response:")
print(result)