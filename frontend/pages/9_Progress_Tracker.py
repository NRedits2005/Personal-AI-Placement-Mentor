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

st.title("📈 Detailed Performance Reports")
st.write("Review details of all completed mock interviews and coding practices.")

headers = get_auth_headers()

tab_interviews, tab_coding = st.tabs(["🤝 Mock Interview Logs", "💻 Coding Submissions"])

with tab_interviews:
    st.subheader("Completed Mock Interviews")
    try:
        response = requests.get(f"{BACKEND_URL}/api/interview/history", headers=headers)
        if response.status_code == 200:
            history = response.json()
            if not history:
                st.info("No mock interviews completed yet.")
            else:
                for idx, session in enumerate(reversed(history)):
                    session_title = f"{idx+1}. {session['interview_type']} Round - Score: {round(session['score'], 1)}%"
                    with st.expander(session_title):
                        st.write(f"**Date:** {session['created_at'][:10]} {session['created_at'][11:16]}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Key Strengths Identified:**")
                            for s in session.get("strengths", []):
                                st.write(f"✅ {s}")
                        with col2:
                            st.write("**Areas of Improvement:**")
                            for w in session.get("weaknesses", []):
                                st.write(f"⚠️ {w}")
                                
                        st.write("**Mentor Feedback Summary:**")
                        for f in session.get("feedback", []):
                            st.write(f"- {f}")
                            
                        # Detailed Q&A
                        st.write("---")
                        st.write("**Question & Answer Breakdown:**")
                        for turn in session.get("questions_answers", []):
                            st.markdown(f"❓ **Question:** {turn['question']}")
                            st.write(f"🗣️ **Your Answer:** {turn['answer']}")
                            st.write(f"⭐ **Score:** {turn.get('score', 0)}/100 | **Feedback:** {turn.get('feedback', 'No feedback recorded.')}")
                            st.write("")
        else:
            st.error("Failed to load interview history.")
    except Exception as e:
        st.error(f"Could not load interview history: {e}")

with tab_coding:
    st.subheader("Coding Submission Logs")
    try:
        c_response = requests.get(f"{BACKEND_URL}/api/coding/progress", headers=headers)
        if c_response.status_code == 200:
            prog = c_response.json()
            solved_qs = prog.get("solved_questions", [])
            
            if not solved_qs:
                st.info("No coding submissions recorded yet.")
            else:
                st.write(f"**Total Questions Solved:** {prog['total_solved']}")
                st.write(f"**Overall Accuracy Rate:** {round(prog['accuracy'], 1)}%")
                st.write(f"**Identified Weak Topics:** {', '.join(prog.get('weak_topics', [])) or 'None'}")
                st.write("---")
                
                for sq in reversed(solved_qs):
                    passed_badge = "✅ Passed" if sq.get("passed") else "❌ Failed"
                    with st.expander(f"Code Submission: {sq.get('title')} ({passed_badge})"):
                        st.write(f"**Timestamp:** {sq.get('timestamp')[:10]} {sq.get('timestamp')[11:16]}")
                        st.write(f"**Logic Correctness Score:** {sq.get('score')}/100")
        else:
            st.error("Failed to load coding progress.")
    except Exception as e:
        st.error(f"Could not load coding logs: {e}")
