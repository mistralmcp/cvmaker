from fastmcp import FastMCP
from src.prompts import CV_WRITER_PROMPT

mcp = FastMCP(name="cvmaker")


@mcp.prompt
def cv_writer():
    """
    Base instructions to follow when extracting the candidate's information for the resumé.
    """

    return CV_WRITER_PROMPT


if __name__ == "__main__":
    mcp.run()
