from rich.console import Console

console = Console(width=120, style="blue on black")
error_console = Console(
    width=100, stderr=True,
    style="bold red on black")
