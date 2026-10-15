"""
resume/skill_editor.py

Human-in-the-loop Skill Editor
Allows users to edit extracted Name, Email and Skills
"""

import streamlit as st


def initialize_resume_session():

    defaults = {
        "resume_name": "",
        "resume_email": "",
        "resume_phone": "",
        "resume_skills": []
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def load_resume_data(resume_data):

    initialize_resume_session()

    st.session_state.resume_name = resume_data.get("name", "")
    st.session_state.resume_email = resume_data.get("email", "")
    st.session_state.resume_phone = resume_data.get("phone", "")
    st.session_state.resume_skills = resume_data.get("skills", [])


def skill_editor():

    initialize_resume_session()

    st.header("Human Verification")

    st.info(
        "Review the extracted information before continuing."
    )

    st.subheader("Basic Information")

    st.session_state.resume_name = st.text_input(
        "Name",
        value=st.session_state.resume_name
    )

    st.session_state.resume_email = st.text_input(
        "Email",
        value=st.session_state.resume_email
    )

    st.session_state.resume_phone = st.text_input(
        "Phone",
        value=st.session_state.resume_phone
    )

    st.divider()

    st.subheader("Extracted Skills")

    skills_text = st.text_input(
        "Skills (comma-separated)",
        value=", ".join(st.session_state.resume_skills)
    )

    st.session_state.resume_skills = [
        s.strip() for s in skills_text.split(",") if s.strip()
    ]

    st.divider()

    if st.button(
        "Save & Continue",
        use_container_width=True
    ):

        return {

            "name": st.session_state.resume_name,

            "email": st.session_state.resume_email,

            "phone": st.session_state.resume_phone,

            "skills": st.session_state.resume_skills
        }

    return None