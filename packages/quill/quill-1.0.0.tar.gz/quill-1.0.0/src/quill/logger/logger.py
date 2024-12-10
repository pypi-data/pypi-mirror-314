from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()
_verbose = False

def set_verbose(verbose: bool) -> None:
    """Set verbose logging mode."""
    global _verbose
    _verbose = verbose

def is_verbose() -> bool:
    """Check if verbose logging is enabled."""
    return _verbose

def debug(message: str) -> None:
    """Log a debug message (only in verbose mode)."""
    if _verbose:
        console.print(f"[dim]{message}[/dim]")

def success(message: str) -> None:
    """Log a success message."""
    console.print(f"[green]{message}[/green]")

def warning(message: str) -> None:
    """Log a warning message."""
    console.print(f"[yellow]Warning: {message}[/yellow]")

def error(message: str, exc_info: bool = False) -> None:
    """Log an error message."""
    console.print(f"[red]Error: {message}[/red]")
    if exc_info and _verbose:
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")

def get_progress() -> Progress:
    """Get a progress context for showing status."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    )