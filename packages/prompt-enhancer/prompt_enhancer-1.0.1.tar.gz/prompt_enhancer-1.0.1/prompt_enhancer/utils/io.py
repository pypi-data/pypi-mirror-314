"""I/O utilities for Prompt Enhancer"""

import json
from datetime import datetime
from ..config import CONFIG

def save_prompt(original: str, enhanced: str, tags: list = None):
    """Save prompt to JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prompt_data = {
        "timestamp": timestamp,
        "original": original,
        "enhanced": enhanced,
        "tags": tags or [],
    }
    
    file_path = CONFIG["PROMPTS_DIR"] / f"prompt_{timestamp}.json"
    with open(file_path, "w") as f:
        json.dump(prompt_data, f, indent=2)
    
    return file_path

def load_prompts():
    """Load all saved prompts."""
    prompts = []
    for file in CONFIG["PROMPTS_DIR"].glob("*.json"):
        with open(file) as f:
            prompts.append(json.load(f))
    return sorted(prompts, key=lambda x: x["timestamp"], reverse=True) 