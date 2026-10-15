"""
job/job_description.py

Handles Job Description input and extracts required skills.
"""

import re
from datetime import date, timedelta

import streamlit as st


# Shared vocabulary - see utils/skills_db.py. This file used to keep
# its own separate copy, so the JD and the resume were matched against
# different skill lists.

from utils.skills_db import SKILL_DATABASE, canonical_skill


def clean_text(text: str):

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_required_skills(job_description: str):

    job_description = job_description.lower()

    detected = []

    for skill in SKILL_DATABASE:

        # Word-boundary match instead of a bare substring test - plain
        # `in` matched "r" inside "your", "go" inside "algorithms",
        # and similar, inventing required skills that weren't there.
        pattern = r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9+#])"

        if re.search(pattern, job_description):

            detected.append(canonical_skill(skill) or skill.title())

    return sorted(set(detected))


def job_description_page():

    if "jd_text" not in st.session_state:
        st.session_state.jd_text = ""

    if "jd_deadline" not in st.session_state:
        # Default a month out, not today - a same-day deadline used to
        # silently make every roadmap/assessment pace calculation
        # collapse to "1 day", no matter how many resources or skills
        # were involved.
        st.session_state.jd_deadline = date.today() + timedelta(days=30)

    st.title("💼 Job Description")

    st.write(
        "Paste the complete Job Description below."
    )

    jd = st.text_area(
        "Job Description",
        height=350,
        placeholder="Paste the job description...",
        value=st.session_state.jd_text
    )

    st.session_state.jd_text = jd

    deadline = st.date_input(
        "Application Deadline",
        value=st.session_state.jd_deadline,
        min_value=date.today() + timedelta(days=1)
    )

    st.session_state.jd_deadline = deadline

    st.caption(
        f"⏳ {(deadline - date.today()).days} day(s) available for "
        "the roadmap and assessment pace to be planned around."
    )

    if st.button(
        "Analyze Job Description",
        use_container_width=True
    ):

        if jd.strip() == "":

            st.error("Please paste the Job Description.")

            return None

        if deadline <= date.today():

            st.error(
                "The deadline must be a future date - otherwise there's "
                "no time left to build a roadmap or take the assessment."
            )

            return None

        cleaned = clean_text(jd)

        skills = extract_required_skills(cleaned)

        result = {

            "job_description": cleaned,

            "required_skills": skills,

            "deadline": str(deadline)
        }

        st.success("Job Description Processed Successfully")

        st.subheader("Detected Skills")

        if skills:

            cols = st.columns(3)

            for i, skill in enumerate(skills):

                with cols[i % 3]:

                    st.success(skill)

        else:

            st.warning("No predefined skills detected.")

        return result

    return None