# Import LangChain agent and tool
from langchain.agents import create_agent
from langchain.tools import tool

# Import Ollama chat model
from langchain_ollama import ChatOllama


# --------------------------------------------------
# MATH TOOL
# --------------------------------------------------

@tool
def calculator(expression: str) -> str:
    """
    Perform basic mathematical calculations.

    Example:
    10 + 5
    20 * 4
    100 / 5
    2 ** 8
    """

    try:
        # Allow only mathematical characters
        allowed_characters = "0123456789+-*/().% "

        for character in expression:
            if character not in allowed_characters:
                return "Invalid mathematical expression."

        # Safely evaluate the mathematical expression
        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception as error:
        return f"Calculation error: {error}"


# --------------------------------------------------
# CREATE OLLAMA MODEL
# --------------------------------------------------

model = ChatOllama(
    model="qwen2.5:0.5b",
    temperature=0
)


# --------------------------------------------------
# AGENT 1 - MATH AGENT
# --------------------------------------------------

math_agent = create_agent(
    model=model,
    tools=[calculator],
    system_prompt=(
        "You are a math agent. "
        "Solve mathematical questions accurately. "
        "Use the calculator tool whenever calculation is needed. "
        "Return a clear final answer."
    )
)


# --------------------------------------------------
# AGENT 2 - REFLECTION AGENT
# --------------------------------------------------

reflection_agent = create_agent(
    model=model,
    tools=[],
    system_prompt=(
        "You are a reflection agent. "
        "You receive a math question and the answer produced by another agent. "
        "Check whether the answer is reasonable and correct. "
        "If it is correct, confirm it. "
        "If it is incorrect, explain the mistake and provide the corrected answer."
    )
)


# --------------------------------------------------
# GET USER QUESTION
# --------------------------------------------------

user_question = input("Enter your math question: ")


# --------------------------------------------------
# RUN FIRST AGENT
# --------------------------------------------------

math_result = math_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": user_question
            }
        ]
    }
)


# Get final response from first agent
math_answer = math_result["messages"][-1].content


# Display first agent result
print("\nMath Agent Response:")
print(math_answer)


# --------------------------------------------------
# SEND OUTPUT TO SECOND AGENT
# --------------------------------------------------

reflection_prompt = f"""
Original math question:

{user_question}

Answer from Math Agent:

{math_answer}

Review this answer and determine whether it is correct.
"""


reflection_result = reflection_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": reflection_prompt
            }
        ]
    }
)


# Get final response from reflection agent
reflection_answer = reflection_result["messages"][-1].content


# --------------------------------------------------
# DISPLAY FINAL REFLECTION
# --------------------------------------------------

print("\nReflection Agent Response:")
print(reflection_answer)