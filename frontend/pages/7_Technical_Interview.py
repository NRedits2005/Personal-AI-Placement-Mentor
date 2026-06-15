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

st.title("💻 Mock Technical Interview")
st.write("Simulate a live engineering interview. Questions are dynamically generated from your resume and GitHub projects.")

# Session States for chat
if "tech_active" not in st.session_state:
    st.session_state.tech_active = False
if "tech_interview_id" not in st.session_state:
    st.session_state.tech_interview_id = None
if "tech_complete" not in st.session_state:
    st.session_state.tech_complete = False

# Action Buttons
col_b1, col_b2 = st.columns(2)
with col_b1:
    if st.button("🚀 Start Technical Interview"):
        headers = get_auth_headers()
        with st.spinner("Initializing mock technical round..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/interview/start",
                    json={"interview_type": "Technical"},
                    headers=headers
                )
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.tech_interview_id = data["interview_id"]
                    st.session_state.tech_active = True
                    st.session_state.tech_complete = False
                else:
                    st.error("Failed to start session. Please upload a resume first.")
            except Exception as e:
                st.error(f"Could not connect to backend server: {e}")

# Fetch active chat history
headers = get_auth_headers()
try:
    history_response = requests.get(f"{BACKEND_URL}/api/interview/active-chat", headers=headers)
    if history_response.status_code == 200:
        chat_data = history_response.json()
        history = chat_data.get("history", [])
        active_type = chat_data.get("interview_type")
        
        # Ensure we are in Technical context
        if active_type == "Technical" and len(history) > 0:
            st.session_state.tech_active = True
            
            # Display Chat logs
            st.write("---")
            for msg in history:
                role = msg["role"]
                content = msg["content"]
                with st.chat_message(role):
                    st.write(content)
                    
            # Check if interview was completed
            user_msg_count = sum(1 for m in history if m["role"] == "user")
            
            if user_msg_count >= 3:
                st.session_state.tech_complete = True
                st.session_state.tech_active = False
                
            # Input response
            if st.session_state.tech_active and not st.session_state.tech_complete:
                user_answer = st.chat_input("Type your response here...", key="tech_ans_input")
                if user_answer:
                    # Submit answer
                    with st.spinner("Evaluating answer..."):
                        try:
                            ans_response = requests.post(
                                f"{BACKEND_URL}/api/interview/{st.session_state.tech_interview_id}/answer",
                                json={"answer": user_answer},
                                headers=headers
                            )
                            if ans_response.status_code == 200:
                                res = ans_response.json()
                                if res["is_complete"]:
                                    st.session_state.tech_complete = True
                                    st.session_state.tech_active = False
                                st.experimental_rerun()
                        except Exception as e:
                            st.error(f"Failed to submit response: {e}")
                            
            if st.session_state.tech_complete:
                st.markdown("---")
                st.success("🎉 Technical Interview Session Completed!")
                st.info("Head to your **Progress Tracker** or the **Dashboard** to view your finalized score reports, strengths, and weaknesses.")
                
        else:
            st.info("Click the button above to launch an interactive Technical interview.")
except Exception as e:
    pass
