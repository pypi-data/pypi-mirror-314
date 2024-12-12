"""Configuration management utilities"""

import os
from pathlib import Path
import json
from rich.prompt import Prompt
from rich.console import Console

console = Console()

CONFIG_DIR = Path.home() / ".prompt_enhancer"
CONFIG_FILE = CONFIG_DIR / "config.json"

def setup_config():
    """Initial configuration setup."""
    CONFIG_DIR.mkdir(exist_ok=True)
    
    if not CONFIG_FILE.exists() or not get_api_key():
        console.print("\n[bold blue]Welcome to Prompt Enhancer![/bold blue]")
        console.print("To get started, you'll need a Groq API key.")
        console.print("You can get one at: [link]https://console.groq.com[/link]")
        
        api_key = Prompt.ask("\nPlease enter your Groq API key", password=True)
        
        config = {
            "GROQ_API_KEY": api_key
        }
        
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
        
        console.print("[green]✓[/green] Configuration saved successfully!")
        return api_key
    
    return get_api_key()

def get_api_key():
    """Get the API key from config file or environment."""
    if os.getenv("GROQ_API_KEY"):
        return os.getenv("GROQ_API_KEY")
        
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                config = json.load(f)
                return config.get("GROQ_API_KEY")
        except:
            return None
            
    return None 