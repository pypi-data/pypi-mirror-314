"""Command-line interface for Prompt Enhancer"""

import sys
import tty
import termios
import pyperclip
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from datetime import datetime
from rich.prompt import Confirm
import json

from .config import CONFIG
from .enhancer import EnhancementStyle, enhance_prompt, analyze_prompt, get_style_prompt
from .utils.display import console, display_suggestions, display_analysis
from .utils.io import save_prompt, load_prompts
from .utils.config_manager import setup_config

class PromptSuggestions:
    def __init__(self, suggestions: list):
        self.suggestions = suggestions
        self.current_index = 0
        self.selected = None

    def next(self):
        """Move to next suggestion."""
        if self.suggestions:
            self.current_index = (self.current_index + 1) % len(self.suggestions)

    def previous(self):
        """Move to previous suggestion."""
        if self.suggestions:
            self.current_index = (self.current_index - 1) % len(self.suggestions)

    def select_current(self):
        """Select current suggestion."""
        if self.suggestions:
            self.selected = self.suggestions[self.current_index]
            return self.selected
        return None

def get_key():
    """Get a single keypress from the user."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

class PromptEnhancer:
    def __init__(self):
        self.session = PromptSession()
        self.current_prompt = None
        self.current_enhanced = None
        self.commands = {
            'enhance': self.cmd_enhance,
            'copy': self.cmd_copy,
            'history': self.cmd_history,
            'move': self.cmd_move,
            'delete': self.cmd_delete,
            'styles': self.cmd_styles,
            'clear': self.cmd_clear,
            'help': self.cmd_help,
            'exit': self.cmd_exit,
            'save': self.cmd_save,
            'analyze': self.cmd_analyze,
            'search': self.cmd_search,
            'export': self.cmd_export,
        }
        command_list = list(self.commands.keys()) + ['/enhance']
        self.command_completer = WordCompleter(command_list)

    def cmd_enhance(self, args):
        """Enhance a prompt with specified style and number of suggestions."""
        if not args:
            console.print("[red]Please provide a prompt to enhance[/red]")
            return

        context_aware = False
        num_suggestions = 1

        if args[0] == '/enhance':
            context_aware = True
            args = args[1:]

        # Check for number of suggestions flag
        for i, arg in enumerate(args):
            if arg.startswith('-') and arg[1:].isdigit():
                num_suggestions = min(CONFIG["MAX_SUGGESTIONS"], max(1, int(arg[1:])))
                args.pop(i)
                break

        if not args:
            console.print("[red]Please provide a prompt to enhance[/red]")
            return

        prompt = " ".join(args)
        style = EnhancementStyle.STANDARD
        
        with console.status("[bold green]Enhancing prompt..." + (" (with workspace context)" if context_aware else "")):
            suggestions = enhance_prompt(prompt, num_suggestions, style, context_aware)
            
        if suggestions:
            self.current_prompt = prompt
            prompt_suggestions = PromptSuggestions(suggestions)
            
            console.print("\n[bold]Original Prompt:[/bold]")
            console.print(Panel(prompt, title="Original", border_style="blue"))
            
            console.print("\n[bold]Enhanced Prompts:[/bold] (Use arrow keys to navigate, Enter to select, q to quit)")
            
            while True:
                console.clear()
                console.print("\n[bold]Original Prompt:[/bold]")
                console.print(Panel(prompt, title="Original", border_style="blue"))
                display_suggestions(suggestions, prompt_suggestions.current_index)
                console.print("\n[dim]← Previous (Left Arrow) | Next (Right Arrow) → | Select (Enter) | Quit (q)[/dim]")
                
                key = get_key()
                
                if key == '\x1b':  # Arrow key prefix
                    key += sys.stdin.read(2)
                    if key == '\x1b[D':  # Left arrow
                        prompt_suggestions.previous()
                    elif key == '\x1b[C':  # Right arrow
                        prompt_suggestions.next()
                elif key == '\r':  # Enter key
                    selected = prompt_suggestions.select_current()
                    if selected:
                        self.current_enhanced = selected
                        console.print("\n[green]Selected prompt:[/green]")
                        console.print(Panel(selected, title="Selected", border_style="green"))
                        save_prompt(prompt, selected)
                    break
                elif key in ('q', 'Q'):
                    break

    def cmd_copy(self, args):
        """Copy current enhanced prompt to clipboard."""
        if self.current_enhanced:
            pyperclip.copy(self.current_enhanced)
            console.print("[green]✓[/green] Copied to clipboard!")
        else:
            console.print("[yellow]No enhanced prompt available to copy[/yellow]")

    def cmd_history(self, args):
        """Show prompt history with optional filtering."""
        limit = 10
        if args and args[0].isdigit():
            limit = int(args[0])
        
        prompts = load_prompts()[:limit]
        if not prompts:
            console.print("[yellow]No prompts in history[/yellow]")
            return

        table = Table(title="Prompt History")
        table.add_column("ID", style="cyan", justify="right")
        table.add_column("Date", style="cyan")
        table.add_column("Original", style="blue")
        table.add_column("Enhanced", style="green")
        table.add_column("Tags", style="magenta")

        for idx, p in enumerate(prompts, 1):
            date = datetime.strptime(p["timestamp"], "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M")
            table.add_row(
                str(idx),
                date,
                p["original"][:50] + "..." if len(p["original"]) > 50 else p["original"],
                p["enhanced"][:50] + "..." if len(p["enhanced"]) > 50 else p["enhanced"],
                ", ".join(p["tags"]) if p["tags"] else ""
            )
        
        console.print(table)

    def cmd_styles(self, args):
        """List available enhancement styles."""
        table = Table(title="Available Enhancement Styles")
        table.add_column("Style", style="cyan")
        table.add_column("Description", style="green")
        
        for style in EnhancementStyle:
            table.add_row(style.value, get_style_prompt(style).split('\n')[0])
        
        console.print(table)

    def cmd_move(self, args):
        """Move to a specific prompt in history by ID."""
        if not args or not args[0].isdigit():
            console.print("[red]Please provide a valid prompt ID[/red]")
            return

        prompts = load_prompts()
        idx = int(args[0]) - 1
        
        if 0 <= idx < len(prompts):
            self.current_prompt = prompts[idx]["original"]
            self.current_enhanced = prompts[idx]["enhanced"]
            console.print("\n[bold]Moved to prompt:[/bold]")
            console.print(Panel(self.current_prompt, title="Original", border_style="blue"))
            console.print(Panel(self.current_enhanced, title="Enhanced", border_style="green"))
        else:
            console.print("[red]Invalid prompt ID[/red]")

    def cmd_delete(self, args):
        """Delete a prompt from history by ID."""
        if not args or not args[0].isdigit():
            console.print("[red]Please provide a valid prompt ID[/red]")
            return

        prompts = load_prompts()
        idx = int(args[0]) - 1
        
        if 0 <= idx < len(prompts):
            prompt = prompts[idx]
            if Confirm.ask(f"Delete prompt from {prompt['timestamp']}?"):
                file_path = CONFIG["PROMPTS_DIR"] / f"prompt_{prompt['timestamp']}.json"
                file_path.unlink()
                console.print("[green]Prompt deleted successfully[/green]")
        else:
            console.print("[red]Invalid prompt ID[/red]")

    def cmd_clear(self, args):
        """Clear the terminal screen."""
        console.clear()

    def cmd_help(self, args):
        """Show help information."""
        help_table = Table(title="Available Commands")
        help_table.add_column("Command", style="cyan")
        help_table.add_column("Description", style="green")
        help_table.add_column("Usage", style="yellow")
        
        commands = {
            'enhance': ('Enhance a prompt', 'enhance "your prompt here" [-2|-3]'),
            '/enhance': ('Context-aware enhancement', '/enhance "your prompt here" [-2|-3]'),
            'copy': ('Copy current prompt to clipboard', 'copy'),
            'history': ('Show prompt history', 'history [limit]'),
            'move': ('Move to a specific prompt', 'move <id>'),
            'delete': ('Delete a prompt', 'delete <id>'),
            'styles': ('List enhancement styles', 'styles'),
            'clear': ('Clear screen', 'clear'),
            'save': ('Save current prompt with tags', 'save [tag1 tag2 ...]'),
            'analyze': ('Analyze prompt quality', 'analyze ["prompt"]'),
            'search': ('Search prompts', 'search <term>'),
            'export': ('Export prompts', 'export <filename>'),
            'exit': ('Exit the program', 'exit'),
        }
        
        for cmd, (desc, usage) in commands.items():
            help_table.add_row(cmd, desc, usage)
        
        console.print(help_table)

    def cmd_save(self, args):
        """Save current prompt with optional tags."""
        if not self.current_prompt or not self.current_enhanced:
            console.print("[yellow]No prompt available to save[/yellow]")
            return

        tags = args if args else []
        file_path = save_prompt(self.current_prompt, self.current_enhanced, tags)
        console.print(f"[green]Saved prompt to {file_path}[/green]")

    def cmd_analyze(self, args):
        """Analyze current or specified prompt."""
        prompt_to_analyze = None
        
        if args:
            prompt_to_analyze = " ".join(args)
        elif self.current_enhanced:
            prompt_to_analyze = self.current_enhanced
        else:
            console.print("[yellow]No prompt available to analyze[/yellow]")
            return

        with console.status("[bold green]Analyzing prompt..."):
            analysis = analyze_prompt(prompt_to_analyze)
            
        if analysis:
            console.print("\n[bold]Prompt Analysis:[/bold]")
            display_analysis(analysis)

    def cmd_search(self, args):
        """Search prompts by keyword."""
        if not args:
            console.print("[red]Please provide a search term[/red]")
            return

        search_term = " ".join(args).lower()
        prompts = load_prompts()
        matches = [p for p in prompts if 
                  search_term in p["original"].lower() or 
                  search_term in p["enhanced"].lower() or
                  any(search_term in tag.lower() for tag in p["tags"])]

        if matches:
            table = Table(title=f"Search Results for '{search_term}'")
            table.add_column("ID", style="cyan", justify="right")
            table.add_column("Original", style="blue")
            table.add_column("Enhanced", style="green")
            
            for idx, p in enumerate(matches, 1):
                table.add_row(
                    str(idx),
                    p["original"][:50] + "..." if len(p["original"]) > 50 else p["original"],
                    p["enhanced"][:50] + "..." if len(p["enhanced"]) > 50 else p["enhanced"]
                )
            
            console.print(table)
        else:
            console.print("[yellow]No matching prompts found[/yellow]")

    def cmd_export(self, args):
        """Export prompts to a file."""
        if not args:
            console.print("[red]Please provide an export filename[/red]")
            return

        filename = args[0]
        prompts = load_prompts()
        
        if filename.endswith('.json'):
            with open(filename, 'w') as f:
                json.dump(prompts, f, indent=2)
        else:
            with open(filename, 'w') as f:
                for p in prompts:
                    f.write(f"Date: {p['timestamp']}\n")
                    f.write(f"Original: {p['original']}\n")
                    f.write(f"Enhanced: {p['enhanced']}\n")
                    f.write(f"Tags: {', '.join(p['tags'])}\n")
                    f.write("-" * 50 + "\n")
        
        console.print(f"[green]Exported {len(prompts)} prompts to {filename}[/green]")

    def cmd_exit(self, args):
        """Exit the program."""
        console.print("[yellow]Goodbye![/yellow]")
        raise SystemExit

    def run(self):
        """Run the interactive prompt enhancer."""
        console.print("[bold blue]Prompt Enhancer Interactive Shell[/bold blue]")
        console.print("Type 'help' for available commands or 'exit' to quit")

        while True:
            try:
                text = self.session.prompt("\n[bold green]prompt-enhancer>[/bold green] ", 
                                         completer=self.command_completer)
                parts = text.strip().split()
                if not parts:
                    continue

                if parts[0].startswith('/'):
                    if parts[0] == '/enhance':
                        self.cmd_enhance(parts)
                    else:
                        console.print(f"[red]Unknown command: {parts[0]}[/red]")
                    continue

                cmd, *args = parts
                if cmd in self.commands:
                    self.commands[cmd](args)
                else:
                    console.print(f"[red]Unknown command: {cmd}[/red]")

            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            except Exception as e:
                console.print(f"[red]Error: {str(e)}[/red]")

def main():
    """Entry point for the command-line interface."""
    # Ensure API key is set up
    api_key = setup_config()
    if not api_key:
        console.print("[red]Error: Groq API key is required to use Prompt Enhancer[/red]")
        console.print("You can get one at: [link]https://console.groq.com[/link]")
        return
    
    # Show welcome message and tips
    console.print("\n[bold blue]🚀 Welcome to Prompt Enhancer![/bold blue]")
    console.print("\nQuick tips:")
    console.print("• Use [cyan]help[/cyan] to see all available commands")
    console.print("• Use [cyan]/enhance[/cyan] for context-aware enhancements")
    console.print("• Use [cyan]enhance -2[/cyan] or [cyan]-3[/cyan] for multiple suggestions")
    console.print("• Your prompts are saved in [cyan]~/.prompt_enhancer/prompts[/cyan]")
    console.print("\nGet started with: [green]enhance \"your prompt here\"[/green]\n")
    
    enhancer = PromptEnhancer()
    enhancer.run()

if __name__ == "__main__":
    main()