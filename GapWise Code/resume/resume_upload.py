"""
resume/resume_upload.py

Handles Resume Upload (PDF/DOCX)
"""

import os
from pathlib import Path

import streamlit as st


UPLOAD_FOLDER = Path("data/resumes")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


ALLOWED_EXTENSIONS = [".pdf", ".docx"]


def save_uploaded_resume(uploaded_file, user_id):
    """
    Save uploaded resume and return file path.
    """

    if uploaded_file is None:
        return None

    extension = os.path.splitext(uploaded_file.name)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        st.error("Only PDF and DOCX files are supported.")
        return None

    filename = f"{user_id}_resume{extension}"

    filepath = UPLOAD_FOLDER / filename

    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return str(filepath)


def resume_upload_page(user_id):
    """
    Resume Upload UI
    """

    st.title("📄 Resume Upload")

    st.write("Upload your Resume (PDF or DOCX)")

    uploaded_file = st.file_uploader(
        "Choose Resume",
        type=["pdf", "docx"]
    )

    if uploaded_file:

        st.write("Filename :", uploaded_file.name)

        st.write(
            "Size :",
            round(uploaded_file.size / 1024, 2),
            "KB"
        )

        # Process immediately on selection - no extra confirmation
        # click required, so nothing looks "stuck" after choosing a file.
        filepath = save_uploaded_resume(
            uploaded_file,
            user_id
        )

        if filepath:

            st.session_state.resume_path = filepath

            return filepath

    return None