import streamlit as st
import requests
import os
from frontend.components.auth import get_auth_headers
from frontend.components.theme import set_page_theme

# Apply global page styling and readability
set_page_theme()

# Auth Guard
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please log in first on the home page.")
    st.stop()

BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

st.title("📅 Study Roadmap Tracker")
st.write("Complete your daily and weekly task schedules to bridge skill gaps. Progress is saved automatically.")

headers = get_auth_headers()
try:
    response = requests.get(f"{BACKEND_URL}/api/roadmap", headers=headers)
    if response.status_code == 200:
        plan = response.json()
        tasks = plan.get("tasks", {})
        completion = plan.get("completion_percentage", 0.0)
        
        # Completion Progress Bar
        st.subheader("📈 Overall Roadmap Progress")
        st.progress(completion / 100.0)
        st.write(f"**{round(completion, 1)}% Completed**")
        
        # Display Tasks Week-by-Week
        st.write("---")
        for week, task_list in tasks.items():
            st.subheader(week)
            for idx, task_item in enumerate(task_list):
                task_desc = task_item["task"]
                completed = task_item["completed"]
                
                # Checkbox input
                key = f"chk_{week}_{idx}"
                checked = st.checkbox(task_desc, value=completed, key=key)
                
                # Update status on change
                if checked != completed:
                    try:
                        update_response = requests.put(
                            f"{BACKEND_URL}/api/roadmap/task",
                            json={"week": week, "task_index": idx, "completed": checked},
                            headers=headers
                        )
                        if update_response.status_code == 200:
                            st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Failed to update task: {e}")
            st.write("")
            
    else:
        st.info("No study roadmap found. Please upload a resume first to generate a personalized roadmap.")
except Exception as e:
    st.error(f"Could not connect to backend server: {e}")
