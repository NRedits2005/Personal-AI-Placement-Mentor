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

st.title("💻 DSA Coding Practice")
st.write("Generate customized coding challenges and receive real-time code quality, correctness, and complexity analyses.")

# Filters
col_f1, col_f2 = st.columns(2)
with col_f1:
    difficulty = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])
with col_f2:
    topic = st.selectbox("Select Topic", ["Arrays", "Strings", "HashMaps", "Linked Lists", "Trees", "Graphs", "Dynamic Programming"])

# Generate/Load Question
if "active_question" not in st.session_state:
    st.session_state.active_question = None

if st.button("🚀 Fetch New Coding Question"):
    headers = get_auth_headers()
    with st.spinner("Generating challenge..."):
        try:
            response = requests.get(
                f"{BACKEND_URL}/api/coding/question",
                params={"difficulty": difficulty, "topic": topic},
                headers=headers
            )
            if response.status_code == 200:
                st.session_state.active_question = response.json()
                st.session_state.eval_results = None
            else:
                st.error("Failed to generate question.")
        except Exception as e:
            st.error(f"Could not connect to backend server: {e}")

# Render Active Question
if st.session_state.active_question:
    q = st.session_state.active_question
    
    st.markdown("---")
    st.subheader(f"📝 {q['title']}")
    
    # Metadata tags
    st.write(f"**Difficulty:** {q['difficulty']} | **Tags:** {', '.join(q['company_tags'])}")
    
    # Description
    st.markdown("### Problem Statement")
    st.write(q["description"])
    
    # Example
    st.markdown("### Examples")
    st.write(f"**Input:** `{q['sample_input']}`")
    st.write(f"**Output:** `{q['sample_output']}`")
    st.write(f"**Constraints:**\n{q['constraints']}")
    
    # Code Input
    st.markdown("### Write Your Code (Python)")
    default_code = "def solve():\n    # Write your solution here\n    pass"
    code_input = st.text_area("Code Editor", value=default_code, height=300, label_visibility="collapsed")
    
    if st.button("Submit Solution"):
        headers = get_auth_headers()
        with st.spinner("Compiling and evaluating solution complexity..."):
            try:
                sub_response = requests.post(
                    f"{BACKEND_URL}/api/coding/submit",
                    json={"question_id": q["question_id"], "code": code_input, "language": "python"},
                    headers=headers
                )
                if sub_response.status_code == 200:
                    st.session_state.eval_results = sub_response.json()
                else:
                    st.error("Submission failed.")
            except Exception as e:
                st.error(f"Could not connect to backend server: {e}")

    # Render Evaluation results
    if "eval_results" in st.session_state and st.session_state.eval_results:
        res = st.session_state.eval_results
        st.markdown("---")
        st.subheader("📊 Evaluation Scorecard")
        
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.metric("Score", f"{res['score']}/100")
        with col_r2:
            st.metric("Time Complexity", res["time_complexity"])
        with col_r3:
            st.metric("Space Complexity", res["space_complexity"])
            
        if res["passed"]:
            st.success("🎉 **Success:** Your code represents a logically complete solution!")
        else:
            st.error("❌ **Failed:** Correctness/logical gaps found in solution.")
            
        st.write(f"**Mentor Feedback:** {res['feedback']}")
        
        if res["suggestions"]:
            st.write("**Improvement Checklist:**")
            for sug in res["suggestions"]:
                st.write(f"- {sug}")
