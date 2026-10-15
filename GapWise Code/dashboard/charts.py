"""
dashboard/charts.py

Interactive Plotly Charts for GapWise Dashboard
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st


# ---------------------------------------------------------
# Skill Match Gauge
# ---------------------------------------------------------

def skill_match_gauge(score: int):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Skill Match %"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#7C3AED"},
                "steps": [
                    {"range": [0, 40], "color": "#EF4444"},
                    {"range": [40, 70], "color": "#F59E0B"},
                    {"range": [70, 100], "color": "#22C55E"},
                ],
            },
        )
    )

    fig.update_layout(
        paper_bgcolor="#1E293B",
        font_color="white",
        height=320,
        margin=dict(l=20, r=20, t=40, b=20),
    )

    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------
# Missing Skills Bar Chart
# ---------------------------------------------------------

def missing_skills_chart(skill_dict):

    if not skill_dict:
        st.info("No Missing Skills.")
        return

    df = pd.DataFrame({
        "Skill": list(skill_dict.keys()),
        "Importance": list(skill_dict.values())
    })

    fig = px.bar(
        df,
        x="Skill",
        y="Importance",
        text="Importance",
    )

    fig.update_layout(
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        font_color="white",
        height=350,
        xaxis_title="Skills",
        yaxis_title="Importance",
    )

    fig.update_traces(
        marker_color="#7C3AED",
        textposition="outside"
    )

    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------
# Skill Distribution Pie Chart
# ---------------------------------------------------------

def skill_distribution(skills):

    if not skills:
        st.info("No skills available.")
        return

    df = pd.DataFrame({
        "Skill": list(skills.keys()),
        "Count": list(skills.values())
    })

    fig = px.pie(
        df,
        values="Count",
        names="Skill",
        hole=0.45
    )

    fig.update_layout(
        paper_bgcolor="#1E293B",
        font_color="white",
        height=350,
    )

    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------
# Roadmap Progress
# ---------------------------------------------------------

def roadmap_progress(progress):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=list(progress.keys()),
            y=list(progress.values()),
            marker_color="#22C55E",
        )
    )

    fig.update_layout(
        title="Learning Progress",
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        font_color="white",
        xaxis_title="Skills",
        yaxis_title="Completion %",
        height=350,
    )

    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------
# Assessment Scores
# ---------------------------------------------------------

def assessment_history(scores):

    if len(scores) == 0:
        st.info("No Assessments Yet.")
        return

    df = pd.DataFrame({
        "Assessment": range(1, len(scores) + 1),
        "Score": scores
    })

    fig = px.line(
        df,
        x="Assessment",
        y="Score",
        markers=True,
    )

    fig.update_layout(
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        font_color="white",
        height=350,
    )

    fig.update_traces(
        line_color="#2563EB",
        marker_size=10
    )

    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------
# Resume Skill Radar
# ---------------------------------------------------------

def radar_chart(skills):

    if not skills:
        st.info("No Skills Found.")
        return

    categories = list(skills.keys())
    values = list(skills.values())

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            line_color="#7C3AED"
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        paper_bgcolor="#1E293B",
        font_color="white",
        height=420,
    )

    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------
# Skill Gap Overview Donut (Matched vs Missing)
# ---------------------------------------------------------

def skill_gap_donut(matched_count, missing_count):

    total = matched_count + missing_count

    if total == 0:
        st.info("No skill gap data yet.")
        return

    fig = go.Figure(
        go.Pie(
            labels=["Matched Skills", "Missing Skills"],
            values=[matched_count, missing_count],
            hole=0.6,
            marker=dict(colors=["#22C55E", "#EF4444"]),
        )
    )

    fig.add_annotation(
        text=f"Total<br>{total}",
        showarrow=False,
        font=dict(color="white", size=16),
    )

    fig.update_layout(
        paper_bgcolor="#1E293B",
        font_color="white",
        height=300,
        margin=dict(l=10, r=10, t=30, b=10),
        showlegend=True,
        legend=dict(orientation="h", y=-0.15),
    )

    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------
# Progress Over Time (per roadmap skill)
# ---------------------------------------------------------

def progress_over_time(roadmap):

    if not roadmap:
        st.info("Generate a roadmap to see progress here.")
        return

    df = pd.DataFrame({
        "Skill": [item["skill"] for item in roadmap],
        "Progress": [item["progress"] for item in roadmap],
    })

    fig = px.line(
        df,
        x="Skill",
        y="Progress",
        markers=True,
    )

    fig.update_layout(
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        font_color="white",
        height=300,
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis_range=[0, 100],
    )

    fig.update_traces(
        line_color="#7C3AED",
        marker=dict(size=9, color="#7C3AED"),
    )

    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------
# Dashboard Summary
# ---------------------------------------------------------

def dashboard_summary(
    skill_match,
    missing_skills,
    roadmap,
    assessments
):

    col1, col2 = st.columns(2)

    with col1:
        skill_match_gauge(skill_match)

    with col2:
        missing_skills_chart(missing_skills)

    col3, col4 = st.columns(2)

    with col3:
        roadmap_progress(roadmap)

    with col4:
        assessment_history(assessments)