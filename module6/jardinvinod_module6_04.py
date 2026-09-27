# Import LangChain agent and tool
from langchain.agents import create_agent
from langchain.tools import tool

# Import Ollama chat model
from langchain_ollama import ChatOllama


# --------------------------------------------------
# CREATE MATH TOOL
# --------------------------------------------------

@tool
def calculator(expression: str) -> str:
    """
    Perform basic mathematical operations.

    Example inputs:
    10 + 5
    20 * 4
    100 / 5
    2 ** 8
    """

    try:
        # Only allow safe mathematical characters
        allowed_characters = "0123456789+-*/().% "

        # Check every character
        for character in expression:
            if character not in allowed_characters:
                return "Invalid mathematical expression."

        # Calculate the result
        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception as error:
        return f"Calculation error: {error}"


# --------------------------------------------------
# CREATE LOCAL OLLAMA LLM
# --------------------------------------------------

model = ChatOllama(
    model="qwen2.5:0.5b",
    temperature=0
)


# --------------------------------------------------
# CREATE LANGCHAIN AGENT
# --------------------------------------------------

agent = create_agent(
    model=model,
    tools=[calculator],
    system_prompt=(
        "You are a math assistant. "
        "Use the calculator tool whenever mathematical "
        "calculation is required."
    )
)


# --------------------------------------------------
# GET QUESTION FROM USER
# --------------------------------------------------

user_question = input(
    "Enter your math question: "
)


# --------------------------------------------------
# RUN AGENT
# --------------------------------------------------

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": user_question
            }
        ]
    }
)


# --------------------------------------------------
# DISPLAY FINAL ANSWER
# --------------------------------------------------

print("\nAgent Response:")

print(
    result["messages"][-1].content
)