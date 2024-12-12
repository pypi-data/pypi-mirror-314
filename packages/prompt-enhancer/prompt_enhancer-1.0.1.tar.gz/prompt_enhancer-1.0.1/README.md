# Prompt Enhancer

An AI-powered CLI tool for enhancing prompts with context awareness and multiple suggestion support.

## Features

- 🧠 AI-powered prompt enhancement
- 🔍 Context-aware suggestions based on workspace analysis
- 🎨 Multiple enhancement styles (Standard, Technical, Creative, etc.)
- 📝 Multiple suggestions with interactive selection
- 📚 Prompt history management
- 🔎 Search and analyze prompts
- 📤 Export functionality

## Installation

### From PyPI
```bash
pip install prompt-enhancer
```

### From Source
```bash
git clone https://github.com/yourusername/prompt-enhancer.git
cd prompt-enhancer
pip install -e .
```

## Configuration

On first run, you'll be prompted to enter your Groq API key.
You can get an API key from [Groq Console](https://console.groq.com).

The API key will be securely saved in `~/.prompt_enhancer/config.json`.

Alternatively, you can set it in your environment:
```bash
export GROQ_API_KEY=your_api_key_here
```

## Usage

Start the interactive shell:
```bash
prompt-enhancer
```

### Available Commands

- `enhance "your prompt"` - Enhance a prompt
- `/enhance "your prompt"` - Context-aware enhancement
- `enhance -2 "your prompt"` - Get 2 suggestions
- `enhance -3 "your prompt"` - Get 3 suggestions
- `copy` - Copy current prompt to clipboard
- `history` - View prompt history
- `search <term>` - Search saved prompts
- `styles` - List enhancement styles
- `analyze` - Analyze current prompt
- `help` - Show all commands

### Enhancement Styles

- `standard` - Clear and effective
- `technical` - Technical specification format
- `creative` - Innovative approaches
- `concise` - Minimal and focused
- `detailed` - Comprehensive breakdown

### Examples

```bash
# Basic enhancement
prompt-enhancer> enhance "create a website"

# Context-aware enhancement
prompt-enhancer> /enhance "create an API endpoint"

# Multiple suggestions
prompt-enhancer> enhance -3 "write a blog post"

# Save with tags
prompt-enhancer> save web development frontend

# Search history
prompt-enhancer> search website
```

## Development

### Setup Development Environment
```bash
# Clone the repository
git clone https://github.com/yourusername/prompt-enhancer.git
cd prompt-enhancer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### Running Tests
```bash
pytest
```

## License

MIT License