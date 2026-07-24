import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from team10_board.services import compute_metrics


def test_metrics_include_blocked_and_overdue():
    tasks = [
        {"status": "todo", "due_date": "2026-07-20"},
        {"status": "blocked", "due_date": "2026-07-30"},
        {"status": "done", "due_date": "2026-07-10"},
        {"status": "in-progress", "due_date": "2026-07-29"},
    ]
    metrics = compute_metrics(tasks)
    assert metrics["total"] == 4
    assert metrics["blocked"] == 1
    assert metrics["done"] == 1
