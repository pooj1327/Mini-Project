"""
dashboard/dashboard.py

Main Dashboard Page
"""

from datetime import datetime, date

import streamlit as st

from dashboard.theme import inject_theme_css, kpi_card, task_row, MUTED
from dashboard.charts import skill_gap_donut, progress_over_time
from dashboard.components import section_title


def _days_left(deadline_str):

    if not deadline_str:
        return None

    try:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
    except Exception:
        return None

    return (deadline - date.today()).days


def _go_to(nav_value):
    """
    Jump to another tab from a Dashboard shortcut button.
    Relies on the main sidebar radio in app.py being bound to
    key="nav_page".
    """

    st.session_state.pending_nav = nav_value

    st.rerun()


def dashboard_page(user):
    """
    Main Dashboard
    """

    inject_theme_css()

    roadmap = st.session_state.get("roadmap") or []

    skill_gap = st.session_state.get("skill_gap") or {}

    assessment_report = st.session_state.get("assessment_report")

    job = st.session_state.get("job") or {}

    resume = st.session_state.get("resume") or {}

    # -----------------------------
    # Header
    # -----------------------------

    section_title(
        f"Welcome back, {user['name'].split(' ')[0]}! 👋",
        "Track your progress and continue your learning journey."
    )

    st.divider()

    # -----------------------------
    # Top KPI Cards
    # -----------------------------

    total_tasks = len(roadmap)

    completed_tasks = len([t for t in roadmap if t.get("completed")])

    overall_progress = (
        round(sum(t.get("progress", 0) for t in roadmap) / total_tasks)
        if total_tasks else 0
    )

    readiness_score = skill_gap.get("readiness_score", 0)

    final_score = (
        assessment_report["final_score"]
        if assessment_report else None
    )

    days_left = _days_left(job.get("deadline"))

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        kpi_card(
            "Overall Progress",
            f"{overall_progress}%",
            "Keep going!" if total_tasks else "Build a roadmap to start",
            icon="🚀",
            color="#7C3AED"
        )

    with c2:
        kpi_card(
            "Skills Completed",
            f"{completed_tasks}",
            f"Out of {total_tasks}" if total_tasks else "No roadmap yet",
            icon="✅",
            color="#22C55E"
        )

    with c3:
        kpi_card(
            "Readiness Score",
            f"{readiness_score}%",
            "Based on skill match" if skill_gap else "Analyze a job first",
            icon="🎯",
            color="#2563EB"
        )

    with c4:
        kpi_card(
            "Latest Assessment",
            f"{final_score}%" if final_score is not None else "--",
            assessment_report["grade"] if assessment_report else "Not attempted",
            icon="📝",
            color="#F59E0B"
        )

    with c5:
        kpi_card(
            "Deadline",
            f"{days_left}d" if days_left is not None else "--",
            "Days left" if days_left is not None else "No deadline set",
            icon="📅",
            color="#EC4899"
        )

    st.divider()

    # -----------------------------
    # Skill Gap / Progress / Upcoming Tasks
    # -----------------------------

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col1:

        st.subheader("Skill Gap Overview")

        matched = len(skill_gap.get("matched_skills", []))

        missing = len(skill_gap.get("missing_skills", []))

        skill_gap_donut(matched, missing)

    with col2:

        st.subheader("Progress Over Time")

        progress_over_time(roadmap)

    with col3:

        st.subheader("Upcoming Tasks")

        pending = [t for t in roadmap if not t.get("completed")]

        pending = sorted(pending, key=lambda t: t.get("end_date", ""))[:4]

        if not pending:

            st.markdown(
                f"<p style='color:{MUTED};'>Nothing pending right now.</p>",
                unsafe_allow_html=True
            )

        else:

            for task in pending:

                task_row(
                    task["skill"],
                    f"Due {task.get('end_date', '--')}",
                    task.get("status", "Not Started")
                )

    st.divider()

    # -----------------------------
    # Recommended Next Steps
    # -----------------------------

    st.subheader("Recommended Next Steps")

    b1, b2, b3, b4 = st.columns(4)

    with b1:
        if st.button("🗺️ Continue Roadmap", use_container_width=True):
            _go_to("🗺️ Roadmap")

    with b2:
        if st.button("📝 Take Assessment", use_container_width=True):
            _go_to("📝 Assessment")

    with b3:
        if st.button("📚 Explore Resources", use_container_width=True):
            _go_to("📚 Resources")

    with b4:
        if st.button("📈 Review Analytics", use_container_width=True):
            _go_to("📈 Analytics")
