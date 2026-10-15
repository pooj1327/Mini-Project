import re
import streamlit as st

from database.database import SessionLocal
from authentication.auth import (
    create_user,
    get_user_by_email
)


# -----------------------------
# Email Validation
# -----------------------------

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'


def valid_email(email):

    return re.match(EMAIL_REGEX, email)


# -----------------------------
# Register Page
# -----------------------------

def register_page():

    st.subheader("📝 Create Account")

    with st.form("register_form"):

        name = st.text_input("Full Name")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        submit = st.form_submit_button("Register")

    if submit:

        if name.strip() == "":
            st.error("Enter your name.")
            return

        if not valid_email(email):
            st.error("Invalid email.")
            return

        if len(password) < 6:
            st.error("Password should contain at least 6 characters.")
            return

        if password != confirm:
            st.error("Passwords do not match.")
            return

        db = SessionLocal()

        existing = get_user_by_email(db, email)

        if existing:
            st.error("Email already registered.")
            db.close()
            return

        create_user(
            db=db,
            name=name,
            email=email,
            password=password
        )

        db.close()

        st.success("Registration Successful!")

        st.info("You can now login.")