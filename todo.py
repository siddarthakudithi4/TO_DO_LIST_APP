import streamlit as st
import uuid
import json
import os

# Initialize session state and load tasks from file
if "tasks" not in st.session_state:
    st.session_state.tasks = []
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as f:
            st.session_state.tasks = json.load(f)

# Function to save tasks to JSON file
def save_tasks():
    with open("tasks.json", "w") as f:
        json.dump(st.session_state.tasks, f, indent=2)

# Custom CSS styling
st.markdown(
    f"""
    <style>
    body {{
        background: #f5f5f5;
        color: #2d2d2d;
        font-family: 'Arial', sans-serif;
    }}

    .task-card {{
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }}

    .completed {{
        text-decoration: line-through;
        color: #888;
    }}

    .priority {{
        display: inline-block;
        padding: 4px 8px;
        border-radius: 15px;
        margin: 5px 0;
        font-size: 0.8em;
    }}
    .high {{ background: #ff5e57; color: white; }}
    .medium {{ background: #ffbc28; color: white; }}
    .low {{ background: #48bb78; color: white; }}

    .stButton button {{
        background: #48bb78;
        color: white;
        border: none;
        border-radius: 20px;
        padding: 8px 20px;
        transition: all 0.3s ease;
    }}
    .stButton button:hover {{
        background: #3498db;
    }}

    .task-actions {{
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }}

    .footer {{
        margin-top: 30px;
        text-align: center;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# App Header
st.markdown('<h1 style="color: #ff5e57; text-align: center;">Todo List 📝</h1>', unsafe_allow_html=True)

# Add Task Form
st.markdown('<div style="background: #fff; padding: 20px; border-radius: 10px; margin-bottom: 20px;">', unsafe_allow_html=True)
with st.form("task_form"):
    task_text = st.text_input("Task description:", placeholder="e.g., Finish project report", key="task_input")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"], key="priority_select")
    due_date = st.date_input("Due Date", key="due_date_picker")
    submitted = st.form_submit_button("Add Task", use_container_width=True)
    
    if submitted and task_text.strip() != "":
        new_task = {
            "id": str(uuid.uuid4()),
            "task": task_text,
            "done": False,
            "priority": priority,
            "due_date": str(due_date),
        }
        st.session_state.tasks.append(new_task)
        save_tasks()
st.markdown('</div>', unsafe_allow_html=True)

# Task Display
for task in st.session_state.tasks.copy():
    col1, col2, col3 = st.columns([4, 1, 1])

    with col1:
        st.markdown(
            f"""
            <div class="task-card">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <strong>{task['task']}</strong>
                        <div class="priority {task['priority'].lower()}">{task['priority']}</div>
                    </div>
                    <div style="color: #888;">
                        Due: {task['due_date']}
                    </div>
                </div>
                <div style="margin-top: 5px;">
                    {task['task']}
                </div>
                <div class="task-actions">
                    <div style="flex: 1;">
                        {task['task']}
                    </div>
                    <div>
                        <strong class="{'completed' if task['done'] else ''}">
                            {'✅ Completed' if task['done'] else '⏳ In Progress'}
                        </strong>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        # Done Status Form
        with st.form(f"task_{task['id']}_done"):
            done = st.checkbox("Mark as Done", value=task["done"], key=f"done_{task['id']}")
            submitted = st.form_submit_button("Save")
            if submitted:
                task["done"] = done
                save_tasks()

    with col3:
        # Delete Button Form
        with st.form(f"task_{task['id']}_delete"):
            if st.form_submit_button("Delete", use_container_width=True):
                st.session_state.tasks.remove(task)
                save_tasks()

        # Edit Button
        if st.button("Edit", key=f"edit_{task['id']}"):
            st.session_state.editing_task = task["id"]

# Edit Form
if "editing_task" in st.session_state:
    task_to_edit = next((t for t in st.session_state.tasks if t["id"] == st.session_state.editing_task), None)
    if task_to_edit:
        with st.form("edit_form"):
            st.header("Edit Task")
            edited_text = st.text_input("Task description:", value=task_to_edit["task"])
            new_priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(task_to_edit["priority"]))
            new_due_date = st.date_input("Due Date", value=task_to_edit["due_date"])
            st.form_submit_button("Save Changes", on_click=lambda: save_edits(task_to_edit, edited_text, new_priority, new_due_date))
            st.form_submit_button("Cancel", on_click=lambda: st.session_state.pop("editing_task", None))

def save_edits(task, text, priority, date):
    task["task"] = text
    task["priority"] = priority
    task["due_date"] = str(date)
    save_tasks()
    st.session_state.pop("editing_task", None)

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
total = len(st.session_state.tasks)
completed = sum(1 for t in st.session_state.tasks if t["done"])
st.write(f"Total Tasks: {total} | Completed: {completed}")
st.progress(completed / total if total else 0, text=f"{int(completed/total*100)}% Complete" if total else "0%")
if st.button("Clear All Tasks", use_container_width=True):
    st.session_state.tasks = []
    save_tasks()
st.markdown('</div>', unsafe_allow_html=True)