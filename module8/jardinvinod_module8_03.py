import json
import urllib.request
import urllib.error

from mcp.server import MCPServer


# ---------------------------------------------------------
# MCP SERVER
# ---------------------------------------------------------

mcp = MCPServer("Ollama MCP Server")


# ---------------------------------------------------------
# OLLAMA SETTINGS
# ---------------------------------------------------------

OLLAMA_URL = "http://localhost:11434/api/generate"

# Change this to a model you already have installed in Ollama
OLLAMA_MODEL = "llama3.2"


# ---------------------------------------------------------
# MCP TOOL
# ---------------------------------------------------------

@mcp.tool()
def ask_ollama(question: str) -> str:
    """
    Send a user question to Ollama and return the generated response.
    """

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": question,
        "stream": False
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

            return result["response"]

    except urllib.error.URLError as error:

        return (
            "Unable to connect to Ollama.\n"
            "Make sure Ollama is running.\n\n"
            f"Error: {error}"
        )

    except KeyError:

        return "Ollama returned a response, but no generated text was found."

    except Exception as error:

        return f"Unexpected error: {error}"


# ---------------------------------------------------------
# START MCP SERVER
# ---------------------------------------------------------

if __name__ == "__main__":
    mcp.run()