# cvmaker

A Python tool to generate professional resumes in PDF format using LaTeX templates.

## Live Server

The service is deployed and accessible at: [https://cvmaker-0c81a29d.alpic.live/](https://cvmaker-0c81a29d.alpic.live/)

## Prerequisites

1. Python 3.10 or higher
2. A LaTeX engine (one of the following):
   - **Tectonic** (recommended) - A self-contained LaTeX engine
   - **latexmk** - Part of a full LaTeX distribution like MacTeX or TexLive

### Installing LaTeX Engine

Choose one of the following methods:

#### Option 1: Tectonic (Recommended)

**macOS:**
- Using Homebrew:
```bash
brew install tectonic
```
- Direct download: [Tectonic for macOS](https://github.com/tectonic-typesetting/tectonic/releases)

**Linux:**
The Tectonic executable is already included in the `bin/` directory of this project. No additional installation is needed.

For manual installation:
```bash
curl --proto '=https' --tlsv1.2 -fsSL https://sh.rustup.rs | sh  # Install Rust first
cargo install tectonic
```

**Windows:**
- Using package managers:
```bash
scoop install tectonic
# or
choco install tectonic
```
- Direct download: [Tectonic for Windows](https://github.com/tectonic-typesetting/tectonic/releases)

#### Option 2: Full LaTeX Distribution

**macOS:**
```bash
brew install --cask mactex
```

**Linux:**
```bash
sudo apt-get install texlive-full latexmk
```

**Windows:**
- Download and install MiKTeX from https://miktex.org/download

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cvmaker.git
cd cvmaker
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Development Setup

For development, you'll need additional packages:

```bash
pip install pytest pytest-mock
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
│   └── utils/
│       ├── pdf.py       # PDF compilation utilities
│       ├── tex.py       # LaTeX rendering utilities
│       ├── storage.py   # Storage utilities
│       └── validation.py # Data validation utilities
├── templates/
│   └── classic.tex.j2   # Default LaTeX template
├── tests/
│   └── __init__.py     # Test package initialization
├── tmp/                # Temporary files directory
├── main.py            # CLI entry point
├── pyproject.toml     # Project configuration
└── README.md          # Project documentation
```