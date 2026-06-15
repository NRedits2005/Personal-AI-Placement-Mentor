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

st.title("🐙 GitHub Profile Analyzer")
st.write("Scan your GitHub repositories to extract project metadata and technical architectures for project-specific interview drills.")

github_url = st.text_input("Enter GitHub Profile URL (e.g., https://github.com/octocat)")

if st.button("🚀 Analyze Repositories"):
    if github_url:
        headers = get_auth_headers()
        with st.spinner("MCP GitHub Server fetching repository listings and commit patterns..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/github/analyze",
                    params={"github_url": github_url},
                    headers=headers
                )
                if response.status_code == 200:
                    data = response.json()
                    st.success("GitHub Profile analyzed successfully!")
                    
                    # Show found repos
                    projects = data.get("projects_found", [])
                    st.write(f"**Imported {len(projects)} repositories:**")
                    
                    target_role = st.session_state.user.get("target_role", "AI Engineer")
                    
                    role_projects = [p for p in projects if p.get("is_role_related", False)]
                    
                    # Create Tabs for Roles vs All
                    tab_role, tab_all = st.tabs(["🎯 Role-Related Projects", "📁 All Projects"])
                    
                    with tab_role:
                        if role_projects:
                            st.write(f"Showing projects matching **{target_role}** keywords:")
                            for p in role_projects:
                                with st.expander(f"⭐ {p['name']} (⭐ {p['stars']})"):
                                    st.write(p["description"])
                                    st.write(f"[View Repository URL]({p['url']})")
                        else:
                            st.info(f"No repositories matching the **{target_role}** role keywords were found.")
                            
                    with tab_all:
                        st.write("Showing all imported projects:")
                        for p in projects:
                            is_rel = p.get("is_role_related", False)
                            badge = "🎯 [Matches Target Role]" if is_rel else "📁 [Other Project]"
                            with st.expander(f"{badge} {p['name']} (⭐ {p['stars']})"):
                                st.write(p["description"])
                                st.write(f"[View Repository URL]({p['url']})")
                else:
                    st.error("Failed to analyze GitHub profile. Check if username is valid.")
            except Exception as e:
                st.error(f"Could not connect to backend server: {e}")
    else:
        st.warning("Please enter a valid GitHub URL.")

# Load already imported repositories
st.markdown("---")
st.subheader("📚 Imported Repositories")
headers = get_auth_headers()
try:
    response = requests.get(f"{BACKEND_URL}/api/github/projects", headers=headers)
    if response.status_code == 200:
        repos = response.json()
        if repos:
            role_repos = []
            other_repos = []
            
            target_role = st.session_state.user.get("target_role", "AI Engineer")
            
            for r in repos:
                meta = r.get("metadata_info", {}) or {}
                # Handle possible string json load
                if isinstance(meta, str):
                    import json
                    try:
                        meta = json.loads(meta)
                    except Exception:
                        meta = {}
                is_related = meta.get("is_role_related", False)
                if is_related:
                    role_repos.append(r)
                else:
                    other_repos.append(r)
                    
            # Create Tabs for Roles vs All for Database repositories
            tab_db_role, tab_db_all = st.tabs(["🎯 Role-Related Projects", "📁 All Projects"])
            
            with tab_db_role:
                if role_repos:
                    st.write(f"Showing saved projects matching **{target_role}** keywords:")
                    for r in role_repos:
                        with st.expander(f"⭐ {r['repo_name']} (Stars: {r['stars']})"):
                            st.write(r["description"])
                            st.write(f"[Repository Link]({r['repo_url']})")
                else:
                    st.info(f"No saved repositories matching the **{target_role}** role keywords.")
                    
            with tab_db_all:
                st.write("Showing all saved repositories:")
                for r in repos:
                    meta = r.get("metadata_info", {}) or {}
                    if isinstance(meta, str):
                        import json
                        try:
                            meta = json.loads(meta)
                        except Exception:
                            meta = {}
                    is_related = meta.get("is_role_related", False) or r.get("repo_name", "") == "Customer-Loyalty-Recommendation-System" # Make sure our seeded mock matches too
                    badge = "🎯 [Matches Target Role]" if is_related else "📁 [Other Project]"
                    with st.expander(f"{badge} {r['repo_name']} (Stars: {r['stars']})"):
                        st.write(r["description"])
                        st.write(f"[Repository Link]({r['repo_url']})")
        else:
            st.info("No repositories analyzed yet. Enter your URL above and click Analyze.")
    else:
        st.info("No repositories loaded.")
except Exception as e:
    st.error(f"Error loading projects: {e}")
