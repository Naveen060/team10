# Team10 Sprint Board

This repository is now a lightweight Streamlit-based team sprint dashboard instead of an empty starter. It helps a small team create tasks, assign owners, track status, and review sprint progress from a simple local interface.

## Features

- Create tasks from the sidebar
- Assign owners and priority levels
- Track `todo`, `in-progress`, and `done` states
- View task metrics at the top of the dashboard
- Persist task data locally in JSON
- Export the task board as JSON
- Delete tasks directly from the dashboard

## Run

```powershell
pip install -r requirements.txt
streamlit run main.py
```

## Notes

- Task data is stored locally in `data/tasks.json`.
- This is intentionally lightweight and works well as a student team project base.
