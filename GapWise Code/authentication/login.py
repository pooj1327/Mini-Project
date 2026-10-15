"""
authentication/login.py

Handles user login, logout, and session initialization.
"""

import streamlit as st
from database.database import SessionLocal
from authentication.auth import authenticate_user


def initialize_session():
    """
    Initialize Streamlit session variables.
    """

    defaults = {
        "logged_in": False,
        "user_id": None,
        "user_name": "",
        "user_email": "",
        "page": "Login"
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def login_user(email: str, password: str):
    """
    Authenticate user credentials.
    """

    db = SessionLocal()

    try:

        user = authenticate_user(
            db,
            email=email,
            password=password
        )

        if user:

            st.session_state.logged_in = True
            st.session_state.user_id = user.id
            st.session_state.user_name = user.name
            st.session_state.user_email = user.email
            st.session_state.page = "Dashboard"

            # Bridge with utils.session, which the rest of the app
            # (app.py's current_user()/is_logged_in()) relies on.
            st.session_state.user = {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }

            return True

        return False

    finally:
        db.close()


def logout():
    """
    Logout current user.
    """

    keys = [
        "logged_in",
        "user_id",
        "user_name",
        "user_email",
        "page"
    ]

    for key in keys:

        if key in st.session_state:
            del st.session_state[key]

    initialize_session()


def login_page():
    """
    Streamlit Login UI.
    """

    initialize_session()

    st.markdown(
        """
        <h2 style='text-align:center;'>
        🔐 Login to GapWise AI
        </h2>
        """,
        unsafe_allow_html=True
    )

    with st.form("login_form"):

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        login_btn = st.form_submit_button(
            "Login"
        )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Create Account"):
            st.session_state.page = "Register"
            st.rerun()

    with col2:
        if st.button("Forgot Password"):
            st.session_state.page = "Forgot Password"
            st.rerun()

    if login_btn:

        if email.strip() == "" or password.strip() == "":
            st.error("Please fill all fields.")
            return

        success = login_user(
            email=email,
            password=password
        )

        if success:

            st.success("Login Successful!")

            st.rerun()

        else:

            st.error("Invalid Email or Password")