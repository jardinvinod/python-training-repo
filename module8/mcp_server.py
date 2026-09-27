import json
import urllib.request
import urllib.error

from mcp.server import MCPServer


# ---------------------------------------------------------
# MCP SERVER
# ---------------------------------------------------------

mcp = MCPServer("Database LLM MCP Server")


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

FASTAPI_CONTEXT_URL = "http://127.0.0.1:8000/context"

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

OLLAMA_MODEL = "llama3.2"


# ---------------------------------------------------------
# GET DATABASE INFORMATION THROUGH FASTAPI
# ---------------------------------------------------------

def get_database_context():
    """
    Call the FastAPI application and retrieve
    information stored in SQLite.
    """

    try:

        with urllib.request.urlopen(
            FASTAPI_CONTEXT_URL
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

            return data.get("records", [])

    except urllib.error.URLError as error:

        raise Exception(
            "Cannot connect to FastAPI server. "
            "Make sure uvicorn is running on port 8000. "
            f"Error: {error}"
        )


# ---------------------------------------------------------
# SEND QUESTION TO OLLAMA
# ---------------------------------------------------------

def call_ollama(question: str, database_records: list):
    """
    Send database information and the user's question
    to Ollama.
    """

    database_text = json.dumps(
        database_records,
        indent=2,
        ensure_ascii=False
    )

    prompt = f"""
You are an assistant that answers questions using
ONLY the database information provided below.

DATABASE INFORMATION:
{database_text}

USER QUESTION:
{question}

Instructions:

1. Answer using information from the database.
2. Do not invent information.
3. If the answer does not exist in the database,
   say: "The information is not available in the database."
4. Give a clear and concise answer.

ANSWER:
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    encoded_data = json.dumps(
        payload
    ).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=encoded_data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:

        with urllib.request.urlopen(
            request
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

            return result.get(
                "response",
                "No response returned from Ollama."
            )

    except urllib.error.URLError as error:

        return (
            "Unable to connect to Ollama. "
            "Make sure Ollama is running.\n"
            f"Error: {error}"
        )


# ---------------------------------------------------------
# MCP TOOL - ASK DATABASE
# ---------------------------------------------------------

@mcp.tool()
def ask_database(question: str) -> str:
    """
    Ask a natural-language question about information
    stored in the SQLite database.
    """

    try:

        database_records = get_database_context()

        if not database_records:
            return "The database currently contains no information."

        answer = call_ollama(
            question,
            database_records
        )

        return answer

    except Exception as error:

        return f"Error: {error}"


# ---------------------------------------------------------
# MCP TOOL - SHOW DATABASE
# ---------------------------------------------------------

@mcp.tool()
def show_database() -> list[dict]:
    """
    Return all information currently stored
    in the SQLite database.
    """

    try:

        return get_database_context()

    except Exception as error:

        return [
            {
                "error": str(error)
            }
        ]


# ---------------------------------------------------------
# START SERVER
# ---------------------------------------------------------

if __name__ == "__main__":
    mcp.run()