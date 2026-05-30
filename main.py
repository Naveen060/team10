import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
TASKS_FILE = DATA_DIR / "tasks.json"


def ensure_storage():
    DATA_DIR.mkdir(exist_ok=True)
    if not TASKS_FILE.exists():
        TASKS_FILE.write_text("[]", encoding="utf-8")


def load_tasks():
    ensure_storage()
    return json.loads(TASKS_FILE.read_text(encoding="utf-8"))


def save_tasks(tasks):
    TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


def add_task(title, owner, priority):
    tasks = load_tasks()
    tasks.append(
        {
            "id": str(uuid4()),
            "title": title,
            "owner": owner,
            "priority": priority,
            "status": "todo",
            "created_at": datetime.utcnow().isoformat(),
        }
    )
    save_tasks(tasks)


def update_task_status(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            break
    save_tasks(tasks)


def metrics(tasks):
    total = len(tasks)
    done = sum(task["status"] == "done" for task in tasks)
    in_progress = sum(task["status"] == "in-progress" for task in tasks)
    return total, in_progress, done


def main():
    st.set_page_config(page_title="Team10 Sprint Board", layout="wide")
    st.title("Team10 Sprint Board")
    st.caption("A lightweight local sprint dashboard for small teams.")

    with st.sidebar:
        st.header("Add Task")
        title = st.text_input("Task title")
        owner = st.text_input("Owner", value="Team Member")
        priority = st.selectbox("Priority", ["high", "medium", "low"], index=1)
        if st.button("Create Task", type="primary") and title.strip():
            add_task(title.strip(), owner.strip() or "Team Member", priority)
            st.success("Task created.")

    tasks = load_tasks()
    total, in_progress, done = metrics(tasks)
    a, b, c = st.columns(3)
    a.metric("Total Tasks", total)
    b.metric("In Progress", in_progress)
    c.metric("Done", done)

    if not tasks:
        st.info("No tasks yet. Add one from the sidebar.")
        return

    status_filter = st.selectbox("Filter by status", ["all", "todo", "in-progress", "done"])
    filtered = [task for task in tasks if status_filter == "all" or task["status"] == status_filter]

    for task in filtered:
        col1, col2, col3 = st.columns([4, 2, 2])
        with col1:
            st.markdown(f"**{task['title']}**")
            st.caption(f"Owner: {task['owner']} | Priority: {task['priority']}")
        with col2:
            new_status = st.selectbox(
                f"Status {task['id']}",
                ["todo", "in-progress", "done"],
                index=["todo", "in-progress", "done"].index(task["status"]),
                label_visibility="collapsed",
            )
        with col3:
            if new_status != task["status"] and st.button(f"Update {task['id'][:8]}"):
                update_task_status(task["id"], new_status)
                st.rerun()
        st.divider()


if __name__ == "__main__":
    main()
