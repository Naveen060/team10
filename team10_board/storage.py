from __future__ import annotations

import json

from .config import DATA_DIR, TASKS_FILE


def ensure_storage() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    if not TASKS_FILE.exists():
        TASKS_FILE.write_text("[]", encoding="utf-8")


def load_records() -> list[dict]:
    ensure_storage()
    return json.loads(TASKS_FILE.read_text(encoding="utf-8"))


def save_records(tasks: list[dict]) -> None:
    TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
