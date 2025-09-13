from fastmcp import FastMCP
from src.prompts import RESUME_INSTRUCTIONS_PROMPT

mcp = FastMCP(name="cvmaker")


@mcp.prompt
def base_instructions():
    """
    Base instructions to follow when extracting the candidate's information for the resumé.
    """

    return RESUME_INSTRUCTIONS_PROMPT


if __name__ == "__main__":
    mcp.run(transport="stdio")
