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

st.title("📊 AI Placement Readiness Score")
st.write("Understand your weighted placement potential and pinpoint preparation channels.")

headers = get_auth_headers()
try:
    response = requests.get(f"{BACKEND_URL}/api/dashboard/summary", headers=headers)
    if response.status_code == 200:
        data = response.json()
        readiness_score = data.get("latest_readiness_score", 0.0)
        
        # Large Card
        st.markdown(f"""
            <div style='background: rgba(30, 41, 59, 0.7); padding: 2rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); text-align: center; margin-bottom: 2rem;'>
                <h2 style='color: #e2e8f0; margin: 0;'>Overall Placement Readiness Score</h2>
                <h1 style='font-size: 4rem; color: #00f2fe; margin: 0.5rem 0;'>{round(readiness_score, 1)}%</h1>
                <p style='color: #94a3b8; font-size: 1.1rem;'>Target Threshold for Top Tier Companies: 85%</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Score Breakdown
        st.subheader("📋 Weighted Component Scorecards")
        
        col_c1, col_c2, col_c3, col_c4, col_c5 = st.columns(5)
        
        # Resume (20%)
        res_score = data["resume"]["resume_score"]
        with col_c1:
            st.metric("Resume Score", f"{res_score}%", help="Weight: 20%")
            st.write(f"Contribution: {round(res_score * 0.2, 1)}%")
            
        # Coding (25%)
        code_score = data["coding"]["accuracy"]
        with col_c2:
            st.metric("Coding Accuracy", f"{round(code_score, 1)}%", help="Weight: 25%")
            st.write(f"Contribution: {round(code_score * 0.25, 1)}%")
            
        # Technical Mock (20%)
        tech_score = data["interviews"]["avg_tech_score"]
        with col_c3:
            st.metric("Technical Mocks", f"{round(tech_score, 1)}%", help="Weight: 20%")
            st.write(f"Contribution: {round(tech_score * 0.2, 1)}%")
            
        # HR Mock (15%)
        hr_score = data["interviews"]["avg_hr_score"]
        with col_c4:
            st.metric("HR Mocks", f"{round(hr_score, 1)}%", help="Weight: 15%")
            st.write(f"Contribution: {round(hr_score * 0.15, 1)}%")
            
        # Projects (20%)
        # Approximate project score based on counts
        project_count = data["projects"]["count"]
        project_score = min(50 + project_count * 15, 100) if project_count > 0 else 0.0
        with col_c5:
            st.metric("Project Score", f"{round(project_score, 1)}%", help="Weight: 20%")
            st.write(f"Contribution: {round(project_score * 0.2, 1)}%")

        st.markdown("---")
        st.subheader("💡 Strategic Mentorship Action Steps")
        
        # Generate automated coaching recommendations based on score margins
        recommendations = []
        if res_score < 85:
            recommendations.append("💼 **Improve Resume Quality:** Your active resume score is under 85%. Go back to the **Upload Resume** page and incorporate all the suggestions given by the Resume Agent.")
        if code_score < 75:
            recommendations.append("💻 **Enhance Coding Accuracy:** Accuracy of solved DSA challenges is low. Visit **Coding Practice** and focus on solving more 'Easy' and 'Medium' level arrays, trees, and dynamic programming tasks.")
        if tech_score < 80:
            recommendations.append("⚙️ **Review Core System Engineering:** Your technical mock averages are under 80%. Review system design concepts (caching, databases, load balancers) and take another **Technical Mock**.")
        if hr_score < 85:
            recommendations.append("🗣️ **Polish Behavioral Speaking:** HR interview confidence ratings can be higher. Practice expressing project timelines using the **STAR** method and attempt another **HR Mock**.")
        if project_count < 2:
            recommendations.append("🐙 **Extend Portfolio Depth:** Import or link more project repositories under the **GitHub Analyzer** page to raise your Project weight contribution.")
            
        if not recommendations:
            st.success("🏆 Incredible work! All your placement preparation benchmarks exceed top-tier targets. You are ready to crack interviews!")
        else:
            for rec in recommendations:
                st.write(rec)
                
    else:
        st.error("Failed to load readiness details from backend.")
except Exception as e:
    st.error(f"Could not connect to backend server: {e}")
