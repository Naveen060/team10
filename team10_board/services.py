from __future__ import annotations

from datetime import UTC, date, datetime
from uuid import uuid4

from .storage import load_records, save_records


DEFAULT_STATUS = "todo"
VALID_STATUSES = ["todo", "in-progress", "blocked", "done"]
VALID_PRIORITIES = ["critical", "high", "medium", "low"]


def load_tasks() -> list[dict]:
    return load_records()


def save_task(title: str, owner: str, priority: str, due_date: str, sprint: str) -> None:
    tasks = load_records()
    tasks.append(
        {
            "id": str(uuid4()),
            "title": title,
            "owner": owner,
            "priority": priority,
            "status": DEFAULT_STATUS,
            "due_date": due_date,
            "sprint": sprint,
            "created_at": datetime.now(UTC).isoformat(),
            "updated_at": datetime.now(UTC).isoformat(),
        }
    )
    save_records(tasks)


def update_task(task_id: str, *, status: str | None = None, owner: str | None = None) -> None:
    tasks = load_records()
    for task in tasks:
        if task["id"] == task_id:
            if status is not None:
                task["status"] = status
            if owner is not None:
                task["owner"] = owner
            task["updated_at"] = datetime.now(UTC).isoformat()
            break
    save_records(tasks)


def delete_task(task_id: str) -> None:
    tasks = [task for task in load_records() if task["id"] != task_id]
    save_records(tasks)


def compute_metrics(tasks: list[dict]) -> dict[str, int]:
    today = date.today()
    done = sum(task["status"] == "done" for task in tasks)
    in_progress = sum(task["status"] == "in-progress" for task in tasks)
    blocked = sum(task["status"] == "blocked" for task in tasks)
    overdue = sum(
        task["status"] != "done" and task.get("due_date") and date.fromisoformat(task["due_date"]) < today
        for task in tasks
    )
    return {
        "total": len(tasks),
        "in_progress": in_progress,
        "blocked": blocked,
        "done": done,
        "overdue": overdue,
    }
