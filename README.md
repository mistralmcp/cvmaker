# cvmaker

MCP server to generate professional resumes in PDF format and return the URL to the PDF.

## MCP Server Connection

Connect to the MCP server from:
- Copy this link : https://cvmaker-0c81a29d.alpic.live/mcp
- Enter the link when creating a connector on: Claude Desktop, ChatGPT, Le Chat

## Prerequisites

1. Python 3.10 or higher
2. Tectonic - A self-contained LaTeX engine

### Installing Tectonic

**macOS:**
```bash
brew install tectonic
```

**Linux:**
The Tectonic executable is already included in the `bin/` directory of this project. No additional installation is needed.

For manual installation:
```bash
curl --proto '=https' --tlsv1.2 -fsSL https://sh.rustup.rs | sh
cargo install tectonic
```

**Windows:**
```bash
scoop install tectonic
# or
choco install tectonic
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mistralmcp/cvmaker.git
cd cvmaker
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies using uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install -r requirements.txt
```

## Project Structure

```
cvmaker/
├── bin/
│   └── tectonic        # Tectonic executable for Linux
├── src/
│   ├── generate.py      # Main resume generation logic
│   ├── models.py        # Pydantic models for data validation
│   ├── instructions.py  # AI instructions and prompts
│   └── utils/          # Various utilities
├── templates/
│   └── classic.tex.j2   # Default LaTeX template
├── main.py            # CLI entry point
└── pyproject.toml     # Project configuration
```