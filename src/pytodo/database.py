"""
Database
"""

import sqlite3
from datetime import datetime

from pytodo.model import Todo

conn = sqlite3.connect("todos.db")
cursor = conn.cursor()


__all__ = ["insert_todo", "get_all_todos", "delete_todo", "complete_todo", "update_todo"]


def create_table() -> None:
    cursor.execute("""CREATE TABLE IF NOT EXISTS todos (
        task text,
        category text,
        date_added text,
        date_completed text,
        status integer,
        position integer
    )""")


create_table()


def insert_todo(todo: Todo) -> None:
    cursor.execute("SELECT COUNT(*) FROM todos")
    count = cursor.fetchone()[0]

    # count will be off by one when count > 0
    todo.position = max(count, 0)

    with conn:
        cursor.execute(
            "INSERT INTO todos VALUES(:task, :category, :date_added, :date_completed, :status, :position)",
            {
                "task": todo.task,
                "category": todo.category,
                "date_added": todo.date_added,
                "date_completed": todo.date_completed,
                "status": todo.status,
                "position": todo.position,
            },
        )


def get_all_todos() -> list[Todo]:
    cursor.execute("SELECT * FROM todos")
    rs = cursor.fetchall()

    todos = [Todo(*result) for result in rs]

    return todos


def delete_todo(position: int) -> None:
    cursor.execute("SELECT COUNT(*) FROM todos")
    count = cursor.fetchone()[0]

    with conn:
        cursor.execute("DELETE FROM todos WHERE position=:position", {"position": position})

        for pos in range(position + 1, count):
            change_position(pos, pos - 1, False)


def change_position(old_position: int, new_position: int, commit: bool = True) -> None:
    cursor.execute(
        "UPDATE todos SET position=:new_position WHERE position=:old_position",
        {"old_position": old_position, "new_position": new_position},
    )

    if commit:
        conn.commit()


def update_todo(position: int, task: str | None, category: str | None) -> None:
    with conn:
        if task and category:
            cursor.execute(
                "UPDATE todos SET task=:task, category=:category WHERE position=:position",
                {"position": position, "task": task, "category": category},
            )

        elif task:
            cursor.execute(
                "UPDATE todos SET task=:task, category=:category WHERE position=:position",
                {"position}": position, "task": task},
            )

        elif category:
            cursor.execute(
                "UPDATE todos SET category=:category WHERE position=:position",
                {"position}": position, "category": category},
            )


def complete_todo(position: int) -> None:
    with conn:
        cursor.execute(
            "UPDATE todos SET status=2, date_completed=:date_completed WHERE position=:position",
            {"position": position, "date_completed": datetime.now().isoformat()},
        )
