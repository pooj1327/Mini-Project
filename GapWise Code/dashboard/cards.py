"""
dashboard/cards.py

Top dashboard KPI cards.
"""

import streamlit as st
from dashboard.components import metric_card


def top_cards(
    skill_match=0,
    readiness_score=0,
    missing_skills=0,
    assessments_completed=0
):
    """
    Display top KPI cards.
    """

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card(
            title="Skill Match",
            value=f"{skill_match}%",
            icon="🎯",
            color="#7C3AED"
        )

    with col2:
        metric_card(
            title="Readiness Score",
            value=f"{readiness_score}%",
            icon="🚀",
            color="#2563EB"
        )

    with col3:
        metric_card(
            title="Missing Skills",
            value=str(missing_skills),
            icon="⚠️",
            color="#F59E0B"
        )

    with col4:
        metric_card(
            title="Assessments",
            value=str(assessments_completed),
            icon="📝",
            color="#22C55E"
        )


def resume_summary_card(
    name,
    email,
    cgpa,
    department,
    skills
):
    """
    Resume summary card.
    """

    skill_tags = ""

    for skill in skills:
        skill_tags += f"""
        <span style="
            background:#334155;
            color:white;
            padding:6px 12px;
            border-radius:20px;
            margin:4px;
            display:inline-block;">
            {skill}
        </span>
        """

    st.markdown(
        f"""
        <div style="
            background:#1E293B;
            padding:25px;
            border-radius:18px;
            margin-top:15px;
        ">

        <h3 style="color:white;">
        👤 Resume Summary
        </h3>

        <hr>

        <p style="color:white;">
        <b>Name:</b> {name}
        </p>

        <p style="color:white;">
        <b>Email:</b> {email}
        </p>

        <p style="color:white;">
        <b>CGPA:</b> {cgpa}
        </p>

        <p style="color:white;">
        <b>Department:</b> {department}
        </p>

        <p style="color:white;">
        <b>Skills</b>
        </p>

        {skill_tags}

        </div>
        """,
        unsafe_allow_html=True,
    )


def quick_statistics(
    completed_courses,
    pending_courses,
    completed_tests,
    roadmap_progress
):
    """
    Small statistics section.
    """

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Completed Courses",
        completed_courses
    )

    c2.metric(
        "Pending Courses",
        pending_courses
    )

    c3.metric(
        "Completed Tests",
        completed_tests
    )

    c4.metric(
        "Roadmap Progress",
        f"{roadmap_progress}%"
    )


def notifications_panel(notifications):
    """
    Notification list.
    """

    st.subheader("🔔 Notifications")

    if not notifications:

        st.info("No new notifications.")

        return

    for note in notifications:

        st.markdown(
            f"""
            <div style="
                background:#312E81;
                padding:15px;
                border-radius:12px;
                margin-bottom:10px;
            ">
            {note}
            </div>
            """,
            unsafe_allow_html=True
        )


def recent_activity(activities):
    """
    Recent user activity.
    """

    st.subheader("📌 Recent Activity")

    if not activities:
        st.info("No activity found.")
        return

    for activity in activities:

        st.markdown(
            f"""
            <div style="
                background:#1E293B;
                padding:12px;
                border-radius:10px;
                margin-bottom:8px;
            ">
            ✅ {activity}
            </div>
            """,
            unsafe_allow_html=True
        )