"""
roadmap/progress_tracker.py

Tracks user progress for the learning roadmap.
"""

import streamlit as st


# --------------------------------------------------
# Initialize Progress
# --------------------------------------------------

def initialize_progress(roadmap):

    if "roadmap" not in st.session_state or st.session_state.roadmap is None:

        st.session_state.roadmap = roadmap


# --------------------------------------------------
# Get Progress
# --------------------------------------------------

def get_progress():

    return st.session_state.get(
        "roadmap",
        []
    ) or []


# --------------------------------------------------
# Mark Skill Completed
# --------------------------------------------------

def mark_completed(index):

    roadmap = get_progress()

    if index < len(roadmap):

        roadmap[index]["completed"] = True

        roadmap[index]["status"] = "Completed"

        roadmap[index]["progress"] = 100

        st.session_state.roadmap = roadmap


# --------------------------------------------------
# Update Progress
# --------------------------------------------------

def update_progress(index, percentage):

    roadmap = get_progress()

    if index >= len(roadmap):

        return

    percentage = max(0, min(100, percentage))

    roadmap[index]["progress"] = percentage

    if percentage == 100:

        roadmap[index]["status"] = "Completed"

        roadmap[index]["completed"] = True

    elif percentage > 0:

        roadmap[index]["status"] = "In Progress"

    else:

        roadmap[index]["status"] = "Pending"

    st.session_state.roadmap = roadmap


# --------------------------------------------------
# Overall Progress
# --------------------------------------------------

def overall_progress():

    roadmap = get_progress()

    if len(roadmap) == 0:

        return 0

    total = sum(skill["progress"] for skill in roadmap)

    return round(total / len(roadmap), 2)


# --------------------------------------------------
# Completed Skills
# --------------------------------------------------

def completed_skills():

    roadmap = get_progress()

    return sum(

        skill["completed"]

        for skill in roadmap

    )


# --------------------------------------------------
# Pending Skills
# --------------------------------------------------

def pending_skills():

    roadmap = get_progress()

    return len(roadmap) - completed_skills()


# --------------------------------------------------
# Display Progress Tracker
# --------------------------------------------------

def display_progress_tracker():

    from dashboard.theme import inject_theme_css

    import plotly.graph_objects as go

    inject_theme_css()

    roadmap = get_progress()

    st.title("📈 Learning Progress")

    if len(roadmap) == 0:

        st.info("No roadmap available.")

        return

    overall = overall_progress()

    st.markdown(
        f'<div style="background:linear-gradient(135deg,#6D28D9,#8B5CF6);'
        f'border-radius:16px;padding:20px;margin-bottom:20px;">'
        f'<div style="color:rgba(255,255,255,.85);font-size:14px;">Overall Progress</div>'
        f'<div style="color:white;font-size:34px;font-weight:700;">{overall}%</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Completed Skills", completed_skills())

    with c2:
        st.metric("Pending Skills", pending_skills())

    st.divider()

    st.subheader("Progress by Skill")

    fig = go.Figure(
        go.Bar(
            x=[s["skill"] for s in roadmap],
            y=[s["progress"] for s in roadmap],
            marker_color=[
                "#22C55E" if s["completed"] else "#7C3AED"
                for s in roadmap
            ],
            text=[f"{s['progress']}%" for s in roadmap],
            textposition="outside"
        )
    )

    fig.update_layout(
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        font_color="white",
        height=280,
        margin=dict(l=10, r=10, t=20, b=10),
        yaxis_range=[0, 110],
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Skill Status")

    st.caption(
        "📍 To mark a skill done or change its progress, go to the "
        "🗺️ Roadmap tab - this page is a read-only summary."
    )

    for skill in roadmap:

        status_emoji = "✅" if skill["completed"] else "🔸"

        st.write(
            f"{status_emoji} **{skill['skill']}** - "
            f"{skill['progress']}% ({skill['status']})"
        )