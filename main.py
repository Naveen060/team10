import csv
import io
from datetime import date

import streamlit as st

from team10_board.services import VALID_PRIORITIES, VALID_STATUSES, compute_metrics, delete_task, load_tasks, save_task, update_task


def export_csv(tasks: list[dict]) -> bytes:
    buffer = io.StringIO()
    writer = csv.DictWriter(
        buffer,
        fieldnames=["title", "owner", "priority", "status", "due_date", "sprint", "created_at", "updated_at"],
    )
    writer.writeheader()
    writer.writerows(tasks)
    return buffer.getvalue().encode("utf-8")


def main():
    st.set_page_config(page_title="Team10 Sprint Board", layout="wide")
    st.title("Team10 Sprint Board")
    st.caption("A lightweight local sprint command center for small teams and student product squads.")

    with st.sidebar:
        st.header("Add Task")
        title = st.text_input("Task title")
        owner = st.text_input("Owner", value="Team Member")
        priority = st.selectbox("Priority", VALID_PRIORITIES, index=2)
        due_date = st.date_input("Due date", value=date.today())
        sprint = st.text_input("Sprint", value="Sprint 1")
        if st.button("Create Task", type="primary") and title.strip():
            save_task(
                title.strip(),
                owner.strip() or "Team Member",
                priority,
                due_date.isoformat(),
                sprint.strip() or "Sprint 1",
            )
            st.success("Task created.")

    tasks = load_tasks()
    metrics = compute_metrics(tasks)
    a, b, c, d, e = st.columns(5)
    a.metric("Total Tasks", metrics["total"])
    b.metric("In Progress", metrics["in_progress"])
    c.metric("Blocked", metrics["blocked"])
    d.metric("Done", metrics["done"])
    e.metric("Overdue", metrics["overdue"])

    if not tasks:
        st.info("No tasks yet. Add one from the sidebar.")
        return

    col_a, col_b, col_c = st.columns([1.4, 1.4, 2.2])
    with col_a:
        status_filter = st.selectbox("Filter by status", ["all", *VALID_STATUSES])
    with col_b:
        sprint_filter = st.selectbox("Filter by sprint", ["all", *sorted({task.get("sprint", "Sprint 1") for task in tasks})])
    with col_c:
        search = st.text_input("Search by title or owner")

    export_bytes = export_csv(tasks)
    st.download_button("Export Sprint CSV", data=export_bytes, file_name="team10_tasks.csv", mime="text/csv")
    filtered = [
        task
        for task in tasks
        if (status_filter == "all" or task["status"] == status_filter)
        and (sprint_filter == "all" or task.get("sprint", "Sprint 1") == sprint_filter)
        and (
            not search.strip()
            or search.strip().lower() in task["title"].lower()
            or search.strip().lower() in task["owner"].lower()
        )
    ]

    for task in filtered:
        col1, col2, col3, col4, col5 = st.columns([4, 2, 2, 2, 1.5])
        with col1:
            st.markdown(f"**{task['title']}**")
            st.caption(
                f"Owner: {task['owner']} | Priority: {task['priority']} | Sprint: {task.get('sprint', 'Sprint 1')} | Due: {task.get('due_date', 'n/a')}"
            )
        with col2:
            new_status = st.selectbox(
                f"Status {task['id']}",
                VALID_STATUSES,
                index=VALID_STATUSES.index(task["status"]),
                label_visibility="collapsed",
            )
        with col3:
            if new_status != task["status"] and st.button(f"Update {task['id'][:8]}"):
                update_task(task["id"], status=new_status)
                st.rerun()
        with col4:
            new_owner = st.text_input(f"Owner {task['id']}", value=task["owner"], label_visibility="collapsed")
            if new_owner != task["owner"] and st.button(f"Reassign {task['id'][:8]}"):
                update_task(task["id"], owner=new_owner.strip() or task["owner"])
                st.rerun()
        with col5:
            if st.button(f"Delete {task['id'][:8]}"):
                delete_task(task["id"])
                st.rerun()
        st.divider()


if __name__ == "__main__":
    main()
