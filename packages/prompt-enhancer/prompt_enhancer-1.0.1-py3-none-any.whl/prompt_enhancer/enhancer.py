"""Core enhancement logic for Prompt Enhancer"""

import os
import groq
import json
from enum import Enum
from typing import List, Dict
import glob
from pathlib import Path
from .config import CONFIG
from .utils.display import console

class EnhancementStyle(str, Enum):
    STANDARD = "standard"
    TECHNICAL = "technical"
    CREATIVE = "creative"
    CONCISE = "concise"
    DETAILED = "detailed"

def get_style_prompt(style: EnhancementStyle) -> str:
    """Get the system prompt for the specified enhancement style."""
    style_prompts = {
        EnhancementStyle.STANDARD: """Enhance the prompt to be clear, concise, and effective.
Focus on clarity and actionable instructions.""",

        EnhancementStyle.TECHNICAL: """Transform the prompt into a technical specification.
Include specific technical requirements, constraints, and acceptance criteria.
Use industry-standard terminology and structured format.""",

        EnhancementStyle.CREATIVE: """Enhance the prompt to encourage creative and innovative solutions.
Expand the possibilities while maintaining the core requirements.
Include elements that inspire unique approaches.""",

        EnhancementStyle.CONCISE: """Create an extremely focused and minimal version of the prompt.
Retain only the most critical requirements.
Use brief, precise language.""",

        EnhancementStyle.DETAILED: """Develop a comprehensive and detailed version of the prompt.
Break down requirements into specific components.
Include all relevant parameters and considerations."""
    }
    return style_prompts[style]

def get_file_content(file_path: str, max_lines: int = 100) -> str:
    """Read file content with line limit."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:max_lines]
            return ''.join(lines)
    except Exception:
        return ""

def get_workspace_context(max_files: int = 5) -> Dict[str, str]:
    """Analyze workspace to gather context."""
    context = {}
    
    important_files = [
        'README.md', 'package.json', 'requirements.txt', 'setup.py',
        '.env.example', 'Dockerfile', 'docker-compose.yml'
    ]

    for filename in important_files:
        if os.path.exists(filename):
            context[filename] = get_file_content(filename)

    file_patterns = ['*.py', '*.js', '*.ts', '*.jsx', '*.tsx', '*.html', '*.css', '*.json']
    all_files = []
    for pattern in file_patterns:
        all_files.extend(glob.glob(f"**/{pattern}", recursive=True))

    excluded_dirs = {'node_modules', 'venv', '.git', '__pycache__', 'dist', 'build'}
    filtered_files = [
        f for f in all_files 
        if not any(d in Path(f).parts for d in excluded_dirs)
    ]

    recent_files = sorted(
        filtered_files,
        key=lambda x: os.path.getmtime(x),
        reverse=True
    )[:max_files]

    for file_path in recent_files:
        if file_path not in context:
            context[file_path] = get_file_content(file_path)

    return context

def create_context_aware_prompt(original_prompt: str, workspace_context: Dict[str, str]) -> str:
    """Create a system prompt that includes workspace context."""
    context_summary = """Analyze the following workspace context:

Project Files:
{}

Based on this context, enhance the following prompt while considering:
1. The project's technical stack and architecture
2. Existing patterns and conventions
3. Related functionality already present
4. Project-specific requirements or constraints

Original prompt: {}"""

    file_summaries = []
    for filename, content in workspace_context.items():
        summary = f"- {filename}: {content[:200]}..." if len(content) > 200 else content
        file_summaries.append(summary)

    return context_summary.format(
        '\n'.join(file_summaries),
        original_prompt
    )

def analyze_prompt(prompt: str) -> dict:
    """Analyze the prompt for quality metrics."""
    system_prompt = """Analyze the given prompt and provide a JSON response with the following metrics:
    - clarity (1-10): How clear and unambiguous is the prompt
    - specificity (1-10): How specific and detailed are the requirements
    - feasibility (1-10): How realistic and achievable are the requirements
    - completeness (1-10): How complete is the information provided
    - suggestions: List of specific improvements (max 3)
    Return ONLY valid JSON."""

    try:
        client = groq.Groq(api_key=CONFIG["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model=CONFIG["DEFAULT_MODEL"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        return json.loads(completion.choices[0].message.content.strip())
    except Exception as e:
        console.print(f"[red]Error analyzing prompt: {str(e)}[/red]")
        return None

def enhance_prompt(original_prompt: str, num_suggestions: int = 1, 
                  style: EnhancementStyle = EnhancementStyle.STANDARD, 
                  context_aware: bool = False) -> list:
    """Enhance the given prompt with multiple suggestions."""
    if not 1 <= num_suggestions <= CONFIG["MAX_SUGGESTIONS"]:
        num_suggestions = 1

    base_prompt = """Enhance the given prompt by refining it to be clear, concise, and relevant.
Provide each enhanced version as a separate, complete prompt.
Do not include numbering or prefixes.
Each suggestion should be self-contained and ready to use.
Focus on making the prompt:
1. Clear and unambiguous
2. Specific and actionable
3. Well-structured and organized
4. Technically precise when needed
5. Appropriately detailed for the task"""

    if context_aware:
        workspace_context = get_workspace_context()
        system_prompt = create_context_aware_prompt(original_prompt, workspace_context)
    else:
        style_prompt = get_style_prompt(style)
        system_prompt = f"{base_prompt}\n\n{style_prompt}\n\nProvide {num_suggestions} different enhanced versions of the prompt."

    try:
        client = groq.Groq(api_key=CONFIG["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model=CONFIG["DEFAULT_MODEL"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Original prompt: {original_prompt}\n\nEnhanced prompts:"}
            ],
            temperature=0.7,
            max_tokens=500 * num_suggestions
        )
        
        response = completion.choices[0].message.content.strip()
        # Split and clean suggestions
        suggestions = [s.strip() for s in response.split('\n\n') 
                      if s.strip() and not s.startswith("Here are")]
        # Remove any numbering
        suggestions = [s.split(".", 1)[1].strip() if s[0].isdigit() and ". " in s else s 
                      for s in suggestions]
        return suggestions[:num_suggestions]
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return None