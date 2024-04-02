"""
Database
"""

from datetime import datetime
from typing import Any, Never, Tuple

import sqlalchemy as db

from pytodo.model import Todo

engine: db.Engine = db.create_engine("sqlite:///todos.db")
metadata: db.MetaData = db.MetaData()


__all__ = ["insert_todo", "get_all_todos", "delete_todo", "complete_todo", "update_todo"]


def create_table(engine: db.Engine, metadata: db.MetaData) -> db.Table | None:
    with engine.connect() as conn:
        if metadata.tables.get("todos", None) is not None:
            return metadata.tables["todos"]

        table: db.Table = db.Table(
            "todos",
            metadata,
            db.Column("task", db.String(255), nullable=False),
            db.Column("category", db.String(255), nullable=False),
            db.Column("date_added", db.String(255), nullable=False),
            db.Column("date_completed", db.String(255), nullable=True),
            db.Column("status", db.Integer(), nullable=False),
            db.Column("position", db.Integer(), nullable=False),
        )
        metadata.create_all(engine)

        conn.commit()

        return table

    return None


todos: db.Table | None = create_table(engine, metadata)


def insert_todo(todo: Todo) -> None:
    with engine.connect() as conn:
        if not engine.dialect.has_table(conn, "todos"):
            # TODO: log error
            return

        table: db.Table = metadata.tables["todos"]

        stmt_count: db.Select[Tuple[int]] | db.Select[Tuple[Never]] = db.select(
            db.func.count(table.c.position)
        ).select_from(table)

        rows: db.CursorResult[Tuple[str, int]] | db.CursorResult[Tuple[Never]] = conn.execute(stmt_count)

        data: db.Row[Tuple[str, int]] | db.Row[Tuple[Never]] | None = rows.first()

        # count is off by one, no need to increment
        todo.position = data[0] if data else 0

        stmt_new: db.Insert = db.insert(metadata.tables["todos"]).values(
            task=todo.task,
            category=todo.category,
            date_added=todo.date_added,
            date_completed=todo.date_completed,
            status=todo.status,
            position=todo.position,
        )

        # comp_new: db.SQLCompiler = stmt_new.compile()

        _: db.CursorResult[Any] = conn.execute(stmt_new)

        conn.commit()


def get_all_todos() -> list[Todo] | None:
    with engine.connect() as conn:
        if not engine.dialect.has_table(conn, "todos"):
            # TODO: log error
            return None

        table: db.Table = metadata.tables["todos"]

        stmt_all: db.Select[Any] = table.select()

        result: db.CursorResult[Any] = conn.execute(stmt_all)

        todos: list[Todo] = [Todo(*row) for row in result.all()]

        return todos

    return None


def delete_todo(position: int) -> None:
    with engine.connect() as conn:
        if not engine.dialect.has_table(conn, "todos"):
            # TODO: log error
            return None

        table: db.Table = metadata.tables["todos"]

        stmt_del: db.Delete = db.delete(table).where(table.c.position == position)

        _: db.CursorResult[Any] = conn.execute(stmt_del)

        conn.commit()

        stmt_count: db.Select[tuple[int]] = db.select(db.func.count()).select_from(table)

        cursor_count: db.CursorResult[Any] = conn.execute(stmt_count)

        result_count: db.Row[Any] | None = cursor_count.first()

        count: int = result_count[0] if result_count else 0

    for pos in range(position + 1, count):
        change_position(pos, pos - 1, False)


def change_position(old_position: int, new_position: int, commit: bool = True) -> None:
    with engine.connect() as conn:
        if not engine.dialect.has_table(conn, "todos"):
            # TODO: log error
            return None

        table: db.Table = metadata.tables["todos"]

        stmt_update: db.Update = db.update(table).where(table.c.position == old_position).values(position=new_position)

        _: db.CursorResult[Any] = conn.execute(stmt_update)

        conn.commit()


def update_todo(position: int, task: str | None, category: str | None) -> None:
    with engine.connect() as conn:
        if not engine.dialect.has_table(conn, "todos"):
            # TODO: log error
            return None

        table: db.Table = metadata.tables["todos"]

        if task and category:
            stmt_update = db.update(table).where(table.c.position == position).values(task=task, category=category)
            _: db.CursorResult[Any] = conn.execute(stmt_update)
            conn.commit()

        elif task:
            stmt_update = db.update(table).where(table.c.position == position).values(task=task)
            _ = conn.execute(stmt_update)
            conn.commit()

        elif category:
            stmt_update = db.update(table).where(table.c.position == position).values(category=category)
            _ = conn.execute(stmt_update)
            conn.commit()


def complete_todo(position: int) -> None:
    with engine.connect() as conn:
        if not engine.dialect.has_table(conn, "todos"):
            # TODO: log error
            return None

        table: db.Table = metadata.tables["todos"]

        stmt_update = (
            db.update(table)
            .where(table.c.position == position)
            .values(status=2, date_completed=datetime.now().isoformat())
        )
        _: db.CursorResult[Any] = conn.execute(stmt_update)
        conn.commit()
