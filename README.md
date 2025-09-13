# cvmaker

A Python tool to generate professional resumes in PDF format using LaTeX templates.

## Prerequisites

1. Python 3.10 or higher
2. A LaTeX engine (one of the following):
   - **Tectonic** (recommended) - A self-contained LaTeX engine
   - **latexmk** - Part of a full LaTeX distribution like MacTeX or TexLive

### Installing LaTeX Engine

Choose one of the following methods:

#### Option 1: Tectonic (Recommended)

**macOS:**
```bash
brew install tectonic
```

**Linux:**
```bash
curl --proto '=https' --tlsv1.2 -fsSL https://sh.rustup.rs | sh  # Install Rust first
cargo install tectonic
```

**Windows:**
```bash
scoop install tectonic
# or
choco install tectonic
```

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

## Running Tests

Run unit tests:
```bash
pytest tests/test_generate.py -v
```

Run integration tests (requires LaTeX engine):
```bash
pytest tests/test_integration.py -v
```

Run all tests:
```bash
pytest -v
```

## Project Structure

```
cvmaker/
├── src/
│   ├── generate.py      # Main resume generation logic
│   ├── models.py        # Pydantic models for data validation
│   ├── prompts.py       # AI prompt templates
│   └── utils/
│       ├── pdf.py       # PDF compilation utilities
│       ├── tex.py       # LaTeX rendering utilities
│       └── validation.py # Data validation utilities
├── templates/
│   └── classic.tex.j2   # Default LaTeX template
├── tests/
│   ├── conftest.py      # Test fixtures
│   ├── test_generate.py # Unit tests
│   └── test_integration.py # Integration tests
└── main.py             # CLI entry point
```