"""
authentication/forgot_password.py

Forgot Password Module
Uses Gmail SMTP + OTP Verification
"""

import os
import random
import smtplib
import streamlit as st

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv

from database.database import SessionLocal
from authentication.auth import get_user_by_email, hash_password

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


# -------------------------------
# Session Initialization
# -------------------------------

def initialize_forgot_session():

    defaults = {
        "otp_sent": False,
        "verified": False,
        "generated_otp": "",
        "reset_email": ""
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# -------------------------------
# OTP Generator
# -------------------------------

def generate_otp():

    return str(random.randint(100000, 999999))


# -------------------------------
# Send OTP
# -------------------------------

def send_otp(email):

    otp = generate_otp()

    subject = "GapWise AI Password Reset OTP"

    body = f"""
Hello,

Your OTP for password reset is:

{otp}

This OTP is valid for one use only.

Regards,
GapWise AI
"""

    msg = MIMEMultipart()

    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        server.sendmail(
            EMAIL_ADDRESS,
            email,
            msg.as_string()
        )

        server.quit()

        st.session_state.generated_otp = otp
        st.session_state.otp_sent = True
        st.session_state.reset_email = email

        return True

    except Exception as e:

        st.error(f"Mail Error : {e}")

        return False


# -------------------------------
# Update Password
# -------------------------------

def update_password(email, new_password):

    db = SessionLocal()

    try:

        user = get_user_by_email(db, email)

        if not user:
            return False

        user.password = hash_password(new_password)

        db.commit()

        return True

    finally:

        db.close()


# -------------------------------
# Forgot Password Page
# -------------------------------

def forgot_password_page():

    initialize_forgot_session()

    st.subheader("🔒 Forgot Password")

    # ---------------------------
    # Step 1
    # ---------------------------

    if not st.session_state.otp_sent:

        email = st.text_input("Registered Email")

        if st.button("Send OTP"):

            db = SessionLocal()

            user = get_user_by_email(db, email)

            db.close()

            if not user:

                st.error("Email not registered.")

            else:

                if send_otp(email):

                    st.success("OTP sent successfully.")

                    st.rerun()

    # ---------------------------
    # Step 2
    # ---------------------------

    elif not st.session_state.verified:

        otp = st.text_input("Enter OTP")

        if st.button("Verify OTP"):

            if otp == st.session_state.generated_otp:

                st.session_state.verified = True

                st.success("OTP Verified")

                st.rerun()

            else:

                st.error("Invalid OTP")

    # ---------------------------
    # Step 3
    # ---------------------------

    else:

        password = st.text_input(
            "New Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Reset Password"):

            if len(password) < 6:

                st.error(
                    "Password should be at least 6 characters."
                )

                return

            if password != confirm:

                st.error(
                    "Passwords do not match."
                )

                return

            updated = update_password(
                st.session_state.reset_email,
                password
            )

            if updated:

                st.success(
                    "Password Updated Successfully!"
                )

                st.session_state.otp_sent = False
                st.session_state.verified = False
                st.session_state.generated_otp = ""
                st.session_state.reset_email = ""

                st.info("You can login now.")

            else:

                st.error("Password update failed.")