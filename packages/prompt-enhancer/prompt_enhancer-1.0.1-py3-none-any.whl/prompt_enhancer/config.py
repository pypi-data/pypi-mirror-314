"""Configuration management for Prompt Enhancer"""

import os
from pathlib import Path
from dotenv import load_dotenv
from .utils.config_manager import setup_config, get_api_key

# Load environment variables
load_dotenv()

# Ensure API key is available
GROQ_API_KEY = get_api_key()

# Base configuration
CONFIG = {
    "GROQ_API_KEY": GROQ_API_KEY,
    "PROMPTS_DIR": Path.home() / ".prompt_enhancer" / "prompts",
    "MAX_SUGGESTIONS": 3,
    "DEFAULT_MODEL": "llama-3.3-70b-specdec",
}

# Ensure prompts directory exists
CONFIG["PROMPTS_DIR"].parent.mkdir(exist_ok=True)
CONFIG["PROMPTS_DIR"].mkdir(exist_ok=True) 