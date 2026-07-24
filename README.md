# Team10 Sprint Board

This repository is now a lightweight but real Streamlit sprint workspace instead of a one-file starter. It gives a small team a local command center for planning, ownership tracking, sprint review, and backlog visibility.

## Features

- Create tasks from the sidebar
- Assign owners, sprint labels, due dates, and priority levels
- Track `todo`, `in-progress`, `blocked`, and `done` states
- View sprint metrics for total, in progress, blocked, done, and overdue work
- Filter by sprint and status, then search by title or owner
- Reassign ownership directly from the board
- Persist task data locally in JSON
- Export the task board as CSV
- Delete tasks directly from the dashboard

## Project Structure

```text
team10/
|-- team10_board/
|   |-- config.py
|   |-- services.py
|   `-- storage.py
|-- tests/
|-- data/
|-- main.py
|-- requirements.txt
`-- README.md
```

## Run

```powershell
pip install -r requirements.txt
streamlit run main.py
```

## Architecture Notes

- `main.py` handles the Streamlit UI only.
- `team10_board/storage.py` manages local JSON persistence.
- `team10_board/services.py` contains task creation, updates, deletion, and sprint metrics.
- `tests/test_services.py` gives the repo a small verification path for backlog analytics.

## Notes

- Task data is stored locally in `data/tasks.json`.
- This is intentionally lightweight and works well as a student team project base.
- The next natural upgrade path is authentication plus a shared database if the team wants multi-user usage.
