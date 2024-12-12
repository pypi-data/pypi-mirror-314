"""Display utilities for Prompt Enhancer"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout

console = Console()

def display_suggestions(suggestions, current_index):
    """Display multiple suggestions with highlighting."""
    for idx, suggestion in enumerate(suggestions):
        is_current = idx == current_index
        border_style = "green" if is_current else "blue"
        title = f"Suggestion {idx + 1}" + (" (Current)" if is_current else "")
        console.print(Panel(suggestion, title=title, border_style=border_style))

def display_analysis(analysis):
    """Display prompt analysis results."""
    if not analysis:
        return

    layout = Layout()
    layout.split_column(
        Layout(Panel(
            Table(
                show_header=True,
                header_style="bold magenta",
                title="Prompt Analysis Metrics"
            ).add_column("Metric").add_column("Score").add_column("Bar"),
            title="Analysis Results"
        )),
        Layout(Panel(
            "\n".join([f"• {s}" for s in analysis.get("suggestions", [])]),
            title="Improvement Suggestions"
        ))
    )

    metrics_table = Table.grid(padding=1)
    metrics = ["clarity", "specificity", "feasibility", "completeness"]
    
    for metric in metrics:
        score = analysis.get(metric, 0)
        bar = "█" * int(score) + "░" * (10 - int(score))
        metrics_table.add_row(
            f"[blue]{metric.title()}[/blue]",
            f"[yellow]{score}[/yellow]",
            f"[green]{bar}[/green]"
        )

    console.print(layout) 