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

st.title("📄 Resume Analysis & Improvement Loop")
st.write("Upload your PDF resume. Our multi-agent squad parses, scores, and refines it until it meets placement standards.")

# Upload Widget
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    if st.button("🚀 Analyze & Optimize Resume"):
        with st.spinner("Multi-agent squad analyzing resume (calculating ATS score, parsing skills)..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            headers = get_auth_headers()
            
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/resume/upload",
                    files=files,
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    onboarding = data["onboarding_results"]
                    
                    st.success("Analysis complete!")
                    
                    col_s1, col_s2 = st.columns(2)
                    with col_s1:
                        st.metric("Resume Quality Score", f"{onboarding['resume_score']}/100")
                    with col_s2:
                        st.metric("ATS Alignment Score", f"{onboarding['ats_score']}/100")
                        
                    # Feedback Loops Alert
                    if onboarding["resume_score"] >= 85:
                        st.balloons()
                        st.success("🎉 Your resume meets standard placement thresholds (>= 85)! Loop completed.")
                    else:
                        st.warning("⚠️ Resume score is below 85. Refinement agent has generated feedback items below to help you upgrade it.")
                        
                    # Extracted Skills
                    st.subheader("💡 Extracted Skills")
                    st.write(", ".join(onboarding["skills"]))
                    
                    # Improvement suggestions
                    st.subheader("🛠️ Recommendations for Improvement")
                    for suggestion in onboarding["improvement_suggestions"]:
                        st.write(f"- {suggestion}")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Failed to analyze resume.')}")
            except Exception as e:
                st.error(f"Could not connect to backend server: {e}")

# Fetch active resume if already uploaded
st.markdown("---")
st.subheader("📂 Active Resume Status")
try:
    headers = get_auth_headers()
    response = requests.get(f"{BACKEND_URL}/api/resume/active", headers=headers)
    if response.status_code == 200:
        active = response.json()
        st.info("A resume is already active on your profile.")
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            st.metric("Active Quality Score", f"{active['resume_score']}/100")
        with col_a2:
            st.metric("Active ATS Score", f"{active['ats_score']}/100")
            
        st.write("**Extracted Skills:**")
        st.write(", ".join(active["extracted_skills"]))
        
        st.write("**Improvement Recommendations:**")
        for sugg in active["improvement_suggestions"]:
            st.write(f"- {sugg}")
    else:
        st.write("No active resume uploaded yet. Use the uploader above to begin onboarding.")
except Exception:
    pass
