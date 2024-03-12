"""
Todo data model.
"""

from datetime import datetime


class Todo:
    def __init__(
        self,
        task: str,
        category: str,
        date_added: str | None = None,
        date_completed: str | None = None,
        status: int | None = None,
        position: int | None = None,
    ):
        self.task = task
        self.category = category

        self.date_added = date_added or datetime.now().isoformat()

        self.date_completed = date_completed or None

        self.status = status or 1  # 1:open, 2:completed

        self.position = position or None

    def __repr__(self) -> str:
        return (
            f"({self.task}, {self.category}, {self.date_added}, {self.date_completed}, {self.status}, {self.position}"
        )
