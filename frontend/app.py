import streamlit as st
import os
from frontend.components.auth import login_user, register_user, logout_user
from frontend.components.theme import set_page_theme

# 1. Page Configuration
st.set_page_config(
    page_title="AI Placement Preparation Mentor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize page styling
set_page_theme()

# Initialize Session States
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None

# Inject Custom CSS for Rich Aesthetics
st.markdown("""
    <style>
    /* Premium Styling and Theming */
    .stApp {
        background: radial-gradient(circle at top right, #1a1b36, #0e1117);
        color: #e2e8f0;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Title and Subtitle */
    .main-title {
        background: linear-gradient(to right, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    .main-subtitle {
        color: #94a3b8;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Glassmorphic Panel */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin: auto;
        max-width: 550px;
    }
    
    /* Custom buttons */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.8rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4);
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 114, 255, 0.6);
        background: linear-gradient(135deg, #0072ff 0%, #00c6ff 100%);
    }
    </style>
""", unsafe_allow_html=True)

# Main Navigation logic
if not st.session_state.logged_in:
    st.markdown("<h1 class='main-title'>🎓 Personal AI Placement Mentor</h1>", unsafe_allow_html=True)
    st.markdown("<p class='main-subtitle'>Accelerate your preparation with Multi-Agent AI, code checkers, and mock interviews.</p>", unsafe_allow_html=True)
    
    # Render Auth form in glassmorphic card container
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        tab_login, tab_register = st.tabs(["🔐 Login", "🚀 Register"])
        
        with tab_login:
            st.write("Welcome back! Please sign in to resume your learning roadmap.")
            email = st.text_input("Email Address", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("Sign In", key="login_btn"):
                if email and password:
                    success, msg = login_user(email, password)
                    if success:
                        st.success(msg)
                        st.experimental_rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Please fill out all fields.")
                    
        with tab_register:
            st.write("Join the platform to unlock customized study schedules and technical interview audits.")
            reg_name = st.text_input("Full Name", key="reg_name")
            reg_email = st.text_input("Email Address", key="reg_email")
            reg_password = st.text_input("Password (min 6 chars)", type="password", key="reg_password")
            
            col_edu1, col_edu2 = st.columns(2)
            with col_edu1:
                reg_college = st.text_input("College / University", key="reg_college")
                reg_grad = st.number_input("Graduation Year", min_value=2020, max_value=2035, value=2026, key="reg_grad")
            with col_edu2:
                reg_dept = st.text_input("Department", key="reg_dept")
                
            col_target1, col_target2 = st.columns(2)
            with col_target1:
                reg_role = st.selectbox(
                    "Target Role",
                    ["AI Engineer", "Software Engineer", "Frontend Engineer", "Backend Engineer", "Full Stack Developer", "Data Scientist"],
                    key="reg_role"
                )
            with col_target2:
                reg_company = st.text_input("Target Company (e.g. Google, Amazon)", key="reg_company")
                
            if st.button("Create Account", key="reg_btn"):
                if reg_name and reg_email and reg_password:
                    if len(reg_password) < 6:
                        st.error("Password must be at least 6 characters.")
                    else:
                        success, msg = register_user(
                            email=reg_email,
                            name=reg_name,
                            password=reg_password,
                            college=reg_college,
                            department=reg_dept,
                            grad_year=int(reg_grad),
                            role=reg_role,
                            company=reg_company
                        )
                        if success:
                            st.success(msg)
                        else:
                            st.error(msg)
                else:
                    st.warning("Please fill out Name, Email, and Password.")
        
        st.markdown("</div>", unsafe_allow_html=True)
else:
    # Sidebar logged in details
    st.sidebar.markdown(f"### 🎓 {st.session_state.user.get('full_name')}")
    st.sidebar.write(f"🎯 **Target Role:** {st.session_state.user.get('target_role')}")
    st.sidebar.write(f"🏢 **Target Company:** {st.session_state.user.get('target_company')}")
    if st.sidebar.button("Log Out"):
        logout_user()
        
    # Welcome Content on successful login
    st.markdown("<h1 class='main-title'>Welcome, Student! 👋</h1>", unsafe_allow_html=True)
    st.markdown("<p class='main-subtitle'>Your path to placement readiness starts here. Use the sidebar pages to navigate.</p>", unsafe_allow_html=True)
    
    st.info("💡 **Getting Started:** First, navigate to the **2_Upload_Resume** page in the sidebar on the left. Once you upload your resume, the system will extract your skills, analyze gaps, and create a customized 3-week study roadmap!")
    
    # Overview of the Multi-Agent Setup
    st.markdown("### 🤖 Your Placement Mentorship Squad")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("📝 Resume & Skill Analyzer")
        st.write("Evaluates your resume against ATS criteria, compares your profile to expected skills, and reveals critical missing components.")
    with col2:
        st.subheader("📅 Study Roadmap Architect")
        st.write("Generates actionable daily and weekly task schedules to bridge your gaps and tracks your study completion history.")
    with col3:
        st.subheader("💻 Coding & Interview Coaches")
        st.write("Conducts simulated technical and HR interviews, evaluates your solutions' complexity, and provides scoring loops.")
