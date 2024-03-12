"""
The cli module
"""

from typing import Optional  # str | None -> not yet supported by typer

import typer
from rich.console import Console
from rich.table import Table

from pytodo import database as db
from pytodo.model import Todo

console = Console()
app = typer.Typer()


@app.command(short_help="adds a todo item")
def add(task: str, category: str) -> None:
    todo: Todo = Todo(task, category)
    db.insert_todo(todo)
    show()


@app.command(short_help="removes a todo item")
def delete(position: int) -> None:
    db.delete_todo(position - 1)
    show()


@app.command(short_help="updates a todo item")
def update(position: int, task: Optional[str] = None, category: Optional[str] = None) -> None:
    db.update_todo(position - 1, task, category)
    show()


@app.command(short_help="removes a todo item")
def complete(position: int) -> None:
    db.complete_todo(position - 1)
    show()


@app.command()
def show() -> None:
    tasks: list[Todo] = db.get_all_todos()

    console.print("[bold magenta]Todos[/bold magenta]!")
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("ToDo", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    def get_category_color(category: str) -> str:
        COLORS: dict[str, str] = {"Learn": "cyan", "YouTube": "red", "Sports": "yellow", "Study": "green"}

        if category in COLORS:
            return COLORS[category]

        return "white"

    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task.category)
        is_done_str = "✅" if task.status == 2 else "❌"
        table.add_row(str(idx), task.task, f"[{c}]{task.category}[/{c}]", is_done_str)

    console.print(table)
