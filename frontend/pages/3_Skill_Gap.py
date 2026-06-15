import streamlit as st
import requests
import os
import pandas as pd
from frontend.components.auth import get_auth_headers
from frontend.components.theme import set_page_theme
from frontend.components.charts import plot_skill_gap

# Apply global page styling and readability
set_page_theme()

# Auth Guard
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please log in first on the home page.")
    st.stop()

BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

st.title("🎯 Skill Gap Analysis")
st.write("Compare your resume's skills against industry expectations for your target role and company.")

headers = get_auth_headers()
try:
    response = requests.get(f"{BACKEND_URL}/api/skill-gap", headers=headers)
    if response.status_code == 200:
        data = response.json()
        skills = data.get("skills", [])
        
        if not skills:
            st.info("No skills evaluated yet. Please upload a resume first.")
        else:
            # Render chart
            fig = plot_skill_gap(skills)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                
            # Render priority list
            st.subheader("📋 Skills Competency Checklist")
            
            # Format DataFrame for Streamlit table display
            df = pd.DataFrame(skills)
            
            # Stylize status for better readability
            def color_status(val):
                color = '#22c55e' if val == 'Present' else '#ef4444'
                return f'color: {color}; font-weight: bold'
                
            def color_priority(val):
                if val == 'High':
                    return 'color: #ef4444; font-weight: bold'
                elif val == 'Medium':
                    return 'color: #f59e0b; font-weight: bold'
                return 'color: #3b82f6; font-weight: bold'

            # Display table
            st.dataframe(
                df.style.map(color_status, subset=['status'])
                        .map(color_priority, subset=['priority']),
                use_container_width=True
            )
            
            # Brief advice
            high_gaps = [item["skill"] for item in skills if item["status"] == "Missing" and item["priority"] == "High"]
            if high_gaps:
                st.error(f"🚨 **Urgent Action Required:** You have **{len(high_gaps)}** High-priority skill gaps remaining: **{', '.join(high_gaps)}**. Head to your study roadmap to begin learning these topics immediately.")
            else:
                st.success("🎉 Excellent! You have filled all high-priority skill requirements for your target role!")
    else:
        st.info("No skill gap analysis found. Go to **Upload Resume** to extract your skills.")
except Exception as e:
    st.error(f"Could not connect to backend server: {e}")
