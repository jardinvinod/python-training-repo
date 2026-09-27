# Import MCPServer - MCP v2
from mcp.server.mcpserver import MCPServer

# Import datetime for system date
from datetime import datetime

# Import random for random number
import random


# --------------------------------------------------
# CREATE MCP SERVER
# --------------------------------------------------

mcp = MCPServer("System Tools Server")


# --------------------------------------------------
# TOOL 1 - SYSTEM DATE
# --------------------------------------------------

@mcp.tool()
def get_system_date() -> str:
    """
    Return the current system date.
    """

    current_date = datetime.now().strftime("%Y-%m-%d")

    return current_date


# --------------------------------------------------
# TOOL 2 - RANDOM NUMBER
# --------------------------------------------------

@mcp.tool()
def get_random_number() -> int:
    """
    Return a random number between 1 and 100.
    """

    return random.randint(1, 100)


# --------------------------------------------------
# RUN MCP SERVER
# --------------------------------------------------

if __name__ == "__main__":
    mcp.run()