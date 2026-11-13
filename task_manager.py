"""Task data model and JSON persistence for the to-do list application."""

import json
import os
import tempfile
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Optional


DATA_FILE = Path(__file__).with_name("tasks.json")


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    due_date: Optional[str] = None
    created_at: str = ""


def load_tasks(path: Path = DATA_FILE) -> list[Task]:
    """Load tasks from JSON, returning an empty list when no file exists yet."""
    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return []

    try:
        records = json.loads(content)
        if not isinstance(records, list):
            raise ValueError("The tasks file must contain a JSON list.")

        tasks = []
        for record in records:
            if not isinstance(record, dict):
                raise ValueError("Each task in the tasks file must be a JSON object.")
            tasks.append(Task(**record))
        return tasks
    except (json.JSONDecodeError, TypeError) as error:
        raise ValueError(f"Could not read tasks from {path}: {error}") from error


def save_tasks(tasks: list[Task], path: Path = DATA_FILE) -> None:
    """Save tasks atomically so an interrupted write does not corrupt the data."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            json.dump([asdict(task) for task in tasks], temporary_file, indent=2)
            temporary_file.write("\n")
        os.replace(temporary_path, path)
    except OSError:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise


def add_task(
    tasks: list[Task],
    title: str,
    description: str = "",
    due_date: Optional[str] = None,
) -> Task:
    title = title.strip()
    if not title:
        raise ValueError("A task title cannot be empty.")
    if due_date:
        try:
            date.fromisoformat(due_date)
        except ValueError as error:
            raise ValueError("Due date must use YYYY-MM-DD format.") from error

    task = Task(
        id=max((item.id for item in tasks), default=0) + 1,
        title=title,
        description=description.strip(),
        due_date=due_date or None,
        created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )
    tasks.append(task)
    return task


def find_task(tasks: list[Task], task_id: int) -> Task:
    for task in tasks:
        if task.id == task_id:
            return task
    raise ValueError(f"No task found with ID {task_id}.")


def update_task(
    tasks: list[Task],
    task_id: int,
    title: str,
    description: str,
    due_date: Optional[str],
) -> Task:
    title = title.strip()
    if not title:
        raise ValueError("A task title cannot be empty.")
    if due_date:
        try:
            date.fromisoformat(due_date)
        except ValueError as error:
            raise ValueError("Due date must use YYYY-MM-DD format.") from error

    task = find_task(tasks, task_id)
    task.title = title
    task.description = description.strip()
    task.due_date = due_date or None
    return task


def delete_task(tasks: list[Task], task_id: int) -> None:
    tasks.remove(find_task(tasks, task_id))
