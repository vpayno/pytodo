"""
The cli module
"""

from typing import Optional  # str | None -> not yet supported by typer

import typer
from rich.console import Console
from rich.table import Table

console = Console()
app = typer.Typer()


@app.command(short_help="adds a todo item")
def add(task: str, category: str) -> None:
    typer.echo(f"adding {task}, {category}")
    show()


@app.command(short_help="removes a todo item")
def delete(position: int) -> None:
    typer.echo(f"deleteing {position}")
    show()


@app.command(short_help="updates a todo item")
def update(position: int, task: Optional[str] = None, category: Optional[str] = None) -> None:
    typer.echo(f"updating {task}, {category}")
    show()


@app.command(short_help="removes a todo item")
def complete(position: int) -> None:
    typer.echo(f"completed {position}")
    show()


@app.command()
def show() -> None:
    tasks = [("Todo1", "Study"), ("Todo2", "Sports")]
    console.print("[bold magenta]Todos[/bold magenta]!")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("ToDo", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    def get_category_color(category: str) -> str:
        COLORS = {"Learn": "cyan", "YouTube": "red", "Sports": "yellow", "Study": "green"}

        if category in COLORS:
            return COLORS[category]

        return "white"

    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task[1])
        is_done_str = "✅" if True else "❌"
        table.add_row(str(idx), task[0], f"[{c}]{task[1]}[/{c}]", is_done_str)

    console.print(table)
