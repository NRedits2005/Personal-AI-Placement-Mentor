import requests
import streamlit as st
import os

# Configure Backend API URL
BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

def get_auth_headers():
    """Helper to return Bearer token headers if logged in."""
    if "token" in st.session_state and st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}

def login_user(email, password):
    """Hits the backend login endpoint."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/auth/login",
            json={"email": email, "password": password}
        )
        if response.status_code == 200:
            token_data = response.json()
            st.session_state.token = token_data.get("access_token")
            st.session_state.logged_in = True
            
            # Fetch user profile
            profile_response = requests.get(
                f"{BACKEND_URL}/api/auth/me",
                headers=get_auth_headers()
            )
            if profile_response.status_code == 200:
                st.session_state.user = profile_response.json()
            return True, "Login successful!"
        else:
            detail = response.json().get("detail", "Invalid credentials.")
            return False, detail
    except Exception as e:
        return False, f"Server connection failed: {e}"

def register_user(email, name, password, college, department, grad_year, role, company):
    """Hits the backend registration endpoint."""
    try:
        payload = {
            "email": email,
            "full_name": name,
            "password": password,
            "college": college if college else None,
            "department": department if department else None,
            "graduation_year": grad_year if grad_year else None,
            "target_role": role if role else "AI Engineer",
            "target_company": company if company else None
        }
        response = requests.post(
            f"{BACKEND_URL}/api/auth/register",
            json=payload
        )
        if response.status_code == 201:
            return True, "Registration successful! You can now log in."
        else:
            detail = response.json().get("detail", "Registration failed.")
            return False, detail
    except Exception as e:
        return False, f"Server connection failed: {e}"

def logout_user():
    """Clears authentication session state keys."""
    st.session_state.token = None
    st.session_state.logged_in = False
    st.session_state.user = None
    st.experimental_rerun()
