import streamlit as st
import requests
import os
from frontend.components.auth import get_auth_headers
from frontend.components.theme import set_page_theme
from frontend.components.charts import (
    plot_readiness_gauge,
    plot_coding_progress,
    plot_readiness_trend,
    plot_weekly_progress
)

# Apply global page styling and readability
set_page_theme()

# Auth Guard
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please log in first on the home page.")
    st.stop()

BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

st.title("📊 Placement Prep Dashboard")

# Fetch dashboard summary
headers = get_auth_headers()
try:
    response = requests.get(f"{BACKEND_URL}/api/dashboard/summary", headers=headers)
    if response.status_code == 200:
        data = response.json()
        
        # High level stats cards
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("Resume Score", f"{data['resume']['resume_score']}/100")
        with col_m2:
            st.metric("Coding Solved", data['coding']['solved'])
        with col_m3:
            st.metric("HR Mock Score", f"{round(data['interviews']['avg_hr_score'], 1)}%")
        with col_m4:
            st.metric("Tech Mock Score", f"{round(data['interviews']['avg_tech_score'], 1)}%")
            
        st.markdown("---")
        
        # Gauge & Trend charts side-by-side
        col_g1, col_g2 = st.columns([1, 2])
        with col_g1:
            gauge_fig = plot_readiness_gauge(data["latest_readiness_score"])
            st.plotly_chart(gauge_fig, use_container_width=True)
        with col_g2:
            trend_data = data["readiness_trend"]
            if trend_data:
                trend_fig = plot_readiness_trend(trend_data)
                st.plotly_chart(trend_fig, use_container_width=True)
            else:
                st.info("Start completing coding challenges or mock interviews to view your readiness trend!")
                
        # Roadmap progress & Coding progress
        st.markdown("---")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            # Fetch roadmap to plot weekly progress
            try:
                roadmap_response = requests.get(f"{BACKEND_URL}/api/roadmap", headers=headers)
                if roadmap_response.status_code == 200:
                    roadmap_data = roadmap_response.json()
                    weekly_fig = plot_weekly_progress(roadmap_data["tasks"])
                    if weekly_fig:
                        st.plotly_chart(weekly_fig, use_container_width=True)
                else:
                    st.info("Upload your resume to construct a study roadmap and track progress.")
            except Exception:
                st.error("Could not load study roadmap progress.")
                
        with col_c2:
            coding_fig = plot_coding_progress(data["coding"]["solved"])
            st.plotly_chart(coding_fig, use_container_width=True)
            
    else:
        st.error("Failed to load dashboard metrics from backend.")
except Exception as e:
    st.error(f"Could not connect to backend server: {e}")
