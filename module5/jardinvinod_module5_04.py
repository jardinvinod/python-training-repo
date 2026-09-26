# Import built-in modules
import json
import urllib.request


# Function to send user input and system prompt to Ollama
def ask_ollama(user_text):

    # Ollama chat API URL
    url = "http://localhost:11434/api/chat"

    # System prompt gives the LLM a persona
    system_prompt = (
        "You are a friendly Python programming teacher. "
        "Explain answers using simple words, short sentences, "
        "and small examples."
    )

    # Data sent to Ollama
    data = {
        "model": "qwen2.5:0.5b",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_text
            }
        ],
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

            # Read response
            response_data = response.read().decode("utf-8")

            # Convert JSON into Python dictionary
            result = json.loads(response_data)

            # Return only the LLM answer
            return result["message"]["content"]

    except Exception as error:

        # Return error if Ollama API fails
        return f"Error: {error}"


# Get input from the user
user_input = input("Enter your question: ")

# Send the question to Ollama
result = ask_ollama(user_input)

# Display the LLM response
print("\nLLM Response:")
print(result)