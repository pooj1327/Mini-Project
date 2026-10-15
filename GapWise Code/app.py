"""
=========================================================
GapWise AI
Intelligent Skill Gap Detection with Human Feedback Loop
=========================================================
"""

import streamlit as st

from streamlit_option_menu import option_menu
from datetime import datetime

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

from config.config import *

# ---------------------------------------------------------
# Utilities
# ---------------------------------------------------------

from utils.session import (
    initialize_session,
    login,
    logout,
    current_user,
    is_logged_in
)

# ---------------------------------------------------------
# Authentication
# ---------------------------------------------------------

from authentication.login import login_page
from authentication.register import register_page
from authentication.forgot_password import forgot_password_page

# ---------------------------------------------------------
# Dashboard
# ---------------------------------------------------------

from dashboard.dashboard import dashboard_page

# ---------------------------------------------------------
# Resume
# ---------------------------------------------------------

from resume.resume_upload import resume_upload_page
from resume.resume_parser import ResumeParser
from resume.skill_extractor import extract_resume_details
from resume.skill_editor import load_resume_data, skill_editor

# ---------------------------------------------------------
# Job
# ---------------------------------------------------------

from job.job_description import job_description_page
from job.skill_gap import run_skill_gap_analysis

# ---------------------------------------------------------
# Resources
# ---------------------------------------------------------

from resources.resource_engine import generate_resource_plan
from resources.resource_selector import display_resources
from resources.recommendation import generate_recommendation

# ---------------------------------------------------------
# Roadmap
# ---------------------------------------------------------

from roadmap.roadmap_generator import generate_learning_roadmap, get_completed_resources
from roadmap.progress_tracker import initialize_progress, display_progress_tracker
from roadmap.adaptive_learning import update_learning_plan

# ---------------------------------------------------------
# Assessment
# ---------------------------------------------------------

from assessment.question_generator import generate_questions
from assessment.mcq_engine import run_mcq_assessment
from assessment.coding_engine import run_coding_assessment
from assessment.evaluator import evaluate_assessment
from assessment.feedback import run_feedback

# ---------------------------------------------------------
# Reports
# ---------------------------------------------------------

from reports.report_generator import generate_report
from reports.pdf_report import create_pdf
from reports.analytics import show_analytics

# ---------------------------------------------------------
# Database
# ---------------------------------------------------------

from database.auth_db import login_user
from database.state_db import save_state, load_state
from database.assessment_db import (
    save_assessment,
    save_feedback,
    get_all_feedback
)

# ---------------------------------------------------------
# Streamlit Configuration
# ---------------------------------------------------------

st.set_page_config(

    page_title="GapWise AI",

    page_icon="🎯",

    layout="wide",

    initial_sidebar_state="expanded"

)

from dashboard.theme import inject_theme_css

inject_theme_css()

# ---------------------------------------------------------
# Theme
# ---------------------------------------------------------

st.markdown("""

<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

.block-container{

padding-top:1rem;

padding-bottom:2rem;

padding-left:2rem;

padding-right:2rem;

}

[data-testid="stSidebar"]{

background:#0F172A;

}

[data-testid="stSidebar"] *{

color:white;

}

div.stButton>button{

width:100%;

border-radius:12px;

height:45px;

font-weight:bold;

}

</style>

""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Initialize Session
# ---------------------------------------------------------

initialize_session()

# ---------------------------------------------------------
# Authentication Router
# ---------------------------------------------------------

if "page" not in st.session_state:

    st.session_state.page = "login"

# ---------------------------------------------------------
# Login
# ---------------------------------------------------------

if not is_logged_in():

    if st.session_state.page == "login":

        login_page()

        # login_page() already renders its own "Create Account" /
        # "Forgot Password" navigation buttons.

    elif st.session_state.page in ("register", "Register"):

        register_page()

        if st.button("Back to Login"):

            st.session_state.page = "login"

            st.rerun()

    elif st.session_state.page in ("forgot", "Forgot Password"):

        forgot_password_page()

        if st.button("Back"):

            st.session_state.page = "login"

            st.rerun()

    st.stop()

# ---------------------------------------------------------
# Logged-in User
# ---------------------------------------------------------

user = current_user()

if user is None:

    logout()

    st.rerun()

# ---------------------------------------------------------
# Restore Saved State
# ---------------------------------------------------------
# Everything the user did before their last logout (resume, job,
# skill gap, selected resources, roadmap + progress, assessment
# questions/answers/report, feedback) lives in the database, not
# just in-memory session state. Reload it once per login so nothing
# is lost when the user logs back in.

if st.session_state.get("_state_hydrated_for") != user["id"]:

    saved = load_state(user["id"])

    for _key, _value in saved.items():
        st.session_state[_key] = _value

    st.session_state._state_hydrated_for = user["id"]

# ---------------------------------------------------------
# Main Application starts here
# ---------------------------------------------------------
# =========================================================
# ADMIN CHECK (feedback is visible to the owner only)
# =========================================================

def is_admin_user(user):

    import os

    admin_email = os.getenv("ADMIN_EMAIL", "").strip().lower()

    if not admin_email or not user:
        return False

    return (user.get("email") or "").strip().lower() == admin_email


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">'
        '<div style="width:44px;height:44px;border-radius:12px;'
        'background:linear-gradient(135deg,#6D28D9,#EC4899);'
        'display:flex;align-items:center;justify-content:center;'
        'font-size:20px;flex-shrink:0;">🎯</div>'
        '<div>'
        '<div style="color:#F1F5F9;font-weight:700;font-size:18px;line-height:1.1;">GapWise AI</div>'
        '<div style="color:#94A3B8;font-size:11px;">Intelligent Skill Gap Detection</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    force_nav = "pending_nav" in st.session_state

    if force_nav:

        st.session_state.nav_page = st.session_state.pop("pending_nav")

    nav_options = [

        "🏠 Dashboard",

        "📄 Resume",

        "💼 Job Description",

        "📚 Resources",

        "🗺️ Roadmap",

        "📊 Progress",

        "📝 Assessment",

        "📈 Analytics",

        "📑 Reports"

    ]

    # The feedback viewer is for the project owner only. It appears in
    # the menu solely when the logged-in account's email matches
    # ADMIN_EMAIL in .env - regular learners never see it.
    if is_admin_user(user):

        nav_options.append("🗨️ Feedback")

    current = st.session_state.get("nav_page", nav_options[0])

    default_index = (
        nav_options.index(current) if current in nav_options else 0
    )

    selected_page = option_menu(

        menu_title=None,

        options=nav_options,

        default_index=default_index,

        manual_select=default_index if force_nav else None,

        styles={

            "container": {
                "padding": "0",
                "background-color": "transparent"
            },

            "icon": {"display": "none"},

            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "2px 0",
                "border-radius": "10px",
                "color": "#CBD5E1",
                "padding": "10px 12px",
                "--hover-color": "#1E293B"
            },

            "nav-link-selected": {
                "background-color": "#7C3AED",
                "color": "white",
                "font-weight": "600"
            }

        }

    )

    st.session_state.nav_page = selected_page

    if force_nav:

        selected_page = current

        st.session_state.nav_page = current

    st.divider()

    journey_steps = [
        ("Resume", bool(st.session_state.get("resume"))),
        ("Job Description", bool(st.session_state.get("job"))),
        ("Resources", bool(st.session_state.get("selected_resources"))),
        ("Roadmap", bool(st.session_state.get("roadmap"))),
        ("Assessment", bool(st.session_state.get("assessment_report"))),
    ]

    journey_done = sum(1 for _, done in journey_steps if done)

    journey_pct = int(journey_done / len(journey_steps) * 100)

    st.markdown(
        f'<div style="font-size:12px;color:#94A3B8;margin-bottom:4px;">'
        f'🚀 Your Journey - {journey_pct}%</div>',
        unsafe_allow_html=True
    )

    st.progress(journey_pct / 100)

    steps_html = "".join(
        f'<span style="font-size:11px;color:{"#22C55E" if done else "#475569"};'
        f'margin-right:8px;">{"✅" if done else "○"} {name}</span>'
        for name, done in journey_steps
    )

    st.markdown(
        f'<div style="line-height:1.9;">{steps_html}</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        f'<div style="background:#1E293B;border:1px solid #243049;'
        f'border-radius:12px;padding:12px 14px;">'
        f'<div style="color:#F1F5F9;font-weight:600;font-size:13px;">👤 {user["name"]}</div>'
        f'<div style="color:#94A3B8;font-size:12px;">📧 {user["email"]}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.write("")

    if st.button("🚪 Logout"):

        logout()

        st.rerun()


# =========================================================
# DASHBOARD
# =========================================================

if selected_page == "🏠 Dashboard":

    dashboard_page(user)


# =========================================================
# RESUME MODULE
# =========================================================

elif selected_page == "📄 Resume":

    st.title("Resume Upload")

    resume_filepath = resume_upload_page(user["id"])

    if resume_filepath is not None:

        with st.spinner("Parsing Resume..."):

            parser = ResumeParser(resume_filepath)

            resume_text = parser.parse()

            name_hint = parser.guess_name()

            parsed_resume = extract_resume_details(resume_text, name_hint=name_hint)

            parsed_resume["resume_text"] = resume_text

        st.session_state.resume = parsed_resume

        save_state(user["id"], resume=parsed_resume)

        load_resume_data(parsed_resume)

        st.success(
            "Resume Parsed Successfully"
        )

    if st.session_state.resume:

        st.divider()

        st.subheader("Extracted Information")

        edited_resume = skill_editor()

        if edited_resume:

            edited_resume["resume_text"] = st.session_state.resume.get(
                "resume_text", ""
            )

            st.session_state.resume = edited_resume

            save_state(user["id"], resume=edited_resume)

            st.success(
                "Resume Saved"
            )

            st.json(
                edited_resume
            )
# =========================================================
# JOB DESCRIPTION MODULE
# =========================================================

elif selected_page == "💼 Job Description":

    st.title("💼 Job Description Analysis")

    job_data = job_description_page()

    if job_data:

        st.session_state.job = job_data

        save_state(user["id"], job=job_data)

    if st.session_state.job and not st.session_state.resume:

        st.warning(
            "Upload your resume first (📄 Resume tab) to see the skill gap analysis."
        )

    if st.session_state.resume and st.session_state.job:

        current_fingerprint = (
            tuple(sorted(st.session_state.resume.get("skills", []))),
            st.session_state.job["job_description"]
        )

        needs_analysis = (
            st.session_state.skill_gap is None
            or st.session_state.get("_skill_gap_fingerprint") != current_fingerprint
        )

        if needs_analysis:

            with st.spinner("Analyzing Skill Gap..."):

                gap_result = run_skill_gap_analysis(

                    st.session_state.resume.get("resume_text", ""),

                    st.session_state.job["job_description"],

                    st.session_state.resume.get("skills", []),

                    st.session_state.job["required_skills"]

                )

            st.session_state.skill_gap = gap_result

            st.session_state._skill_gap_fingerprint = current_fingerprint

            save_state(user["id"], skill_gap=gap_result)

        gap_result = st.session_state.skill_gap

        st.success("Analysis Completed")

        c1, c2 = st.columns(2)

        with c1:

            st.subheader("✅ Matched Skills")

            if gap_result["matched_skills"]:

                for skill in gap_result["matched_skills"]:

                    st.success(skill)

            else:

                st.info("No Matched Skills")

        with c2:

            st.subheader("❌ Missing Skills")

            if gap_result["missing_skills"]:

                for skill in gap_result["missing_skills"]:

                    st.error(skill)

            else:

                st.success("No Missing Skills")

        st.divider()

        c1, c2 = st.columns(2)

        c1.metric(

            "Skill Match",

            f"{gap_result['skill_match']}%"

        )

        c2.metric(

            "Readiness Score",

            f"{gap_result['readiness_score']}%"

        )

        if gap_result.get("extra_skills"):

            st.divider()

            st.subheader("⭐ Additional Skills")

            st.write(", ".join(gap_result["extra_skills"]))


# =========================================================
# RESOURCE RECOMMENDATION MODULE
# =========================================================

elif selected_page == "📚 Resources":

    st.title("📚 Personalized Learning Resources")

    if st.session_state.skill_gap is None:

        st.warning(

            "Please complete Skill Gap Analysis first."

        )

        st.stop()

    missing_skills = st.session_state.skill_gap["missing_skills"]

    if len(missing_skills) == 0:

        st.success(

            "No missing skills detected."

        )

        st.stop()

    feedback_level = (
        st.session_state.feedback.get("difficulty")
        if st.session_state.get("feedback") else None
    )

    with st.spinner(

        "Generating Dynamic Resources..."

    ):

        resources = generate_resource_plan(

            missing_skills,

            level=feedback_level

        )

    if feedback_level:

        st.info(
            f"📋 Resources re-ranked for your feedback level: **{feedback_level}**"
        )

    st.session_state.resources = resources

    st.subheader(

        "Choose Your Preferred Resources"

    )

    selected_resources = display_resources(

        resources

    )

    st.session_state.selected_resources = selected_resources

    save_state(user["id"], selected_resources=selected_resources)

    st.divider()

    st.subheader(

        "🎯 AI Recommendation"

    )

    recommendation = generate_recommendation(

        missing_skills,

        selected_resources,

        st.session_state.job["deadline"],

        st.session_state.assessment_report["final_score"]
        if st.session_state.assessment_report else 0,

        st.session_state.feedback["difficulty"]
        if st.session_state.feedback else "Medium"

    )

    st.session_state.recommendation = recommendation

    st.info(

        recommendation["recommendation"]

    )

    st.caption(

        f"Suggested pace : {recommendation['study_hours_per_day']} "
        f"hrs/day for {recommendation['days_remaining']} day(s) "
        f"· Level : {recommendation['learning_level']}"

    )

    st.divider()

    total_selected = sum(len(v) for v in selected_resources.values())

    skills_with_pick = sum(1 for v in selected_resources.values() if v)

    if total_selected == 0:

        st.warning(

            "No resources selected yet - check at least one resource "
            "per skill above before generating your roadmap."

        )

    else:

        st.success(

            f"{total_selected} resource(s) selected across "
            f"{skills_with_pick} of {len(missing_skills)} skill(s)."

        )

    if st.button(

        "Generate Learning Roadmap",

        use_container_width=True

    ):

        st.session_state.pending_nav = "🗺️ Roadmap"

        st.rerun()
# =========================================================
# ROADMAP MODULE
# =========================================================

elif selected_page == "🗺️ Roadmap":

    st.title("🗺️ Personalized Learning Roadmap")

    if st.session_state.get("selected_resources") is None:

        st.warning(
            "Please select learning resources first."
        )

        st.stop()

    if len(st.session_state.selected_resources) == 0:

        st.warning(
            "Select at least one resource."
        )

        st.stop()

    roadmap_fingerprint = (
        tuple(sorted(st.session_state.skill_gap["missing_skills"])),
        tuple(sorted(st.session_state.selected_resources.keys())),
        st.session_state.job["deadline"]
    )

    needs_roadmap = (
        st.session_state.roadmap is None
        or st.session_state.get("_roadmap_fingerprint") != roadmap_fingerprint
    )

    if needs_roadmap:

        with st.spinner(
            "Generating AI Roadmap..."
        ):

            roadmap = generate_learning_roadmap(

                st.session_state.skill_gap["missing_skills"],

                st.session_state.selected_resources,

                st.session_state.job["deadline"]

            )

        st.session_state.roadmap = roadmap

        st.session_state._roadmap_fingerprint = roadmap_fingerprint

        save_state(user["id"], roadmap=roadmap)

    roadmap = st.session_state.roadmap

    st.success(
        "Roadmap Generated Successfully"
    )

    st.divider()

    overall_progress = 0

    completed_topics = 0

    total_topics = len(roadmap)

    for index, task in enumerate(roadmap):

        with st.container():

            col1, col2 = st.columns([5,1])

            with col1:

                status_colors = {
                    "Completed": "#22C55E",
                    "In Progress": "#2563EB",
                    "Pending": "#F59E0B",
                }

                color = status_colors.get(task["status"], "#94A3B8")

                st.markdown(
                    f'<div style="background:#1E293B;border:1px solid #243049;'
                    f'border-left:4px solid {color};border-radius:12px;'
                    f'padding:14px 16px;margin-bottom:8px;">'
                    f'<div style="color:#F1F5F9;font-weight:700;font-size:16px;">{task["skill"]}</div>'
                    f'<div style="color:#94A3B8;font-size:13px;margin-top:4px;">'
                    f'📅 {task["start_date"]} → {task["end_date"]} &nbsp;·&nbsp; '
                    f'📚 {len(task["resources"])} resource(s)'
                    f'</div>'
                    f'<div style="color:{color};font-size:12px;font-weight:600;margin-top:6px;">'
                    f'● {task["status"]}'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            with col2:

                completed = st.checkbox(

                    "Done",

                    value=task["completed"],

                    key=f"task_{index}",

                    help="Marks every resource under this skill as completed."

                )

            # ------------------------------------------------
            # Per-resource completion.
            # The assessment generates questions ONLY from the
            # resources ticked here, so each resource needs its
            # own completion state - a single skill-level tick
            # isn't granular enough to scope questions properly.
            # ------------------------------------------------

            task_resources = roadmap[index].get("resources", [])

            if task_resources:

                with st.expander(
                    f"📚 Mark completed resources for {task['skill']}",
                    expanded=not task["completed"]
                ):

                    st.caption(
                        "Tick each resource you've actually finished. "
                        "Your assessment questions are generated only "
                        "from these."
                    )

                    for r_index, resource in enumerate(task_resources):

                        # "Done" at the skill level force-completes
                        # everything beneath it.
                        default_done = (
                            True if completed
                            else resource.get("completed", False)
                        )

                        resource_done = st.checkbox(

                            f"{resource.get('title', 'Resource')} "
                            f"· _{resource.get('platform', '')}_",

                            value=default_done,

                            key=f"res_{index}_{r_index}"

                        )

                        roadmap[index]["resources"][r_index]["completed"] = (
                            resource_done
                        )

            # Skill progress is derived from how many of its
            # resources are done, so partial progress is real
            # rather than just 0 or 100.

            done_count = sum(
                1 for r in roadmap[index].get("resources", [])
                if r.get("completed")
            )

            total_count = len(roadmap[index].get("resources", []))

            if total_count > 0:

                roadmap[index]["progress"] = round(
                    (done_count / total_count) * 100
                )

            elif completed:

                roadmap[index]["progress"] = 100

            else:

                roadmap[index]["progress"] = 0

            roadmap[index]["completed"] = (
                roadmap[index]["progress"] >= 100
            )

            if roadmap[index]["completed"]:

                roadmap[index]["status"] = "Completed"

                completed_topics += 1

            else:

                roadmap[index]["status"] = (
                    "In Progress"
                    if roadmap[index]["progress"] > 0
                    else "Pending"
                )

            overall_progress += roadmap[index]["progress"]

    overall_progress = round(

        overall_progress /

        total_topics

    )

    st.session_state.roadmap = roadmap

    save_state(user["id"], roadmap=roadmap)

    st.divider()

    st.success(

        f"{completed_topics}/{total_topics} Skills Completed &nbsp;·&nbsp; "
        f"See the 📊 Progress tab for detailed tracking and charts."

    )

    if completed_topics == total_topics:

        st.success(

            "Congratulations! Learning Roadmap Completed."

        )
# =========================================================
# PROGRESS PAGE
# =========================================================

elif selected_page == "📊 Progress":

    st.title("📊 Progress Tracker")

    if "roadmap" not in st.session_state:

        st.warning(
            "Roadmap not generated."
        )

        st.stop()

    initialize_progress(st.session_state.roadmap)

    display_progress_tracker()

    st.divider()

    completed = len(

        [

            i

            for i in st.session_state.roadmap

            if i["completed"]

        ]

    )

    total = len(

        st.session_state.roadmap

    )

    percentage = round(

        completed /

        total *

        100,

        2

    ) if total else 0

    c1, c2, c3 = st.columns(3)

    c1.metric(

        "Completed",

        completed

    )

    c2.metric(

        "Pending",

        total-completed

    )

    c3.metric(

        "Completion",

        f"{percentage}%"

    )

    st.progress(

        percentage/100

    )

    st.divider()

    if percentage >= 100:

        st.success(

            "Ready for Assessment"

        )

    else:

        st.info(

            "Complete remaining skills before taking assessment."

        )
# =========================================================
# ASSESSMENT MODULE
# =========================================================

elif selected_page == "📝 Assessment":

    st.title("📝 Skill Assessment")

    if st.session_state.get("roadmap") is None:

        st.warning(
            "Complete your roadmap first."
        )

        st.stop()

    completed = len(

        [

            i

            for i in st.session_state.roadmap

            if i["completed"]

        ]

    )

    total = len(st.session_state.roadmap)

    # -------------------------------------------------
    # Scope: only resources ticked as COMPLETED feed the
    # assessment. Selecting a resource at the start is not
    # enough - the learner has to have finished it.
    # -------------------------------------------------

    completed_resources = get_completed_resources(
        st.session_state.roadmap
    )

    completed_resource_count = sum(
        len(v) for v in completed_resources.values()
    )

    if completed_resource_count == 0:

        st.warning(

            "No completed resources yet. Go to the 🗺️ Roadmap tab and "
            "tick the resources you've finished - your assessment is "
            "generated only from those."

        )

        st.stop()

    st.info(

        f"📚 Assessment scoped to **{completed_resource_count} completed "
        f"resource(s)** across **{len(completed_resources)} skill(s)**: "
        + ", ".join(completed_resources.keys())

    )

    with st.expander("See exactly which resources questions come from"):

        for _skill, _resources in completed_resources.items():

            st.markdown(f"**{_skill}**")

            for _r in _resources:

                st.markdown(
                    f"- {_r.get('title', 'Resource')} "
                    f"· _{_r.get('platform', '')}_"
                )

    if completed == total:

        st.success(

            "Roadmap Completed."

    )

    st.divider()

    # -------------------------------------------------
    # Generate Questions
    # -------------------------------------------------

    # If the learner ticks more resources as completed, the previously
    # generated questions no longer match their scope - regenerate.

    assessment_fingerprint = tuple(sorted(

        (skill, tuple(sorted(r.get("title", "") for r in resources)))

        for skill, resources in completed_resources.items()

    ))

    needs_questions = (

        not st.session_state.get("assessment_questions")

        or st.session_state.get("_assessment_fingerprint")
            != assessment_fingerprint

    )

    if needs_questions:

        with st.spinner(

            "Generating Questions..."

        ):

            st.session_state.assessment_questions = generate_questions(

                st.session_state.skill_gap,

                completed_resources

            )

            st.session_state._assessment_fingerprint = assessment_fingerprint

            save_state(user["id"], assessment_questions=st.session_state.assessment_questions)

    if st.button("🔄 Get New Questions (Retake)"):

        st.session_state.assessment_questions = generate_questions(

            st.session_state.skill_gap,

            completed_resources

        )

        st.session_state._assessment_fingerprint = assessment_fingerprint

        st.session_state.mcq_answers = {}

        st.session_state.coding_answers = {}

        st.session_state.mcq_report = None

        st.session_state.coding_report = None

        st.session_state.assessment_report = None

        save_state(

            user["id"],

            assessment_questions=st.session_state.assessment_questions,

            mcq_answers={},

            coding_answers={},

            assessment_report=None

        )

        st.rerun()

    questions = st.session_state.assessment_questions

    if questions.get("used_fallback"):

        if questions.get("no_key_configured"):

            st.info(
                "No GOOGLE_API_KEY is configured, so these are placeholder "
                "questions rather than real AI-generated ones. Add "
                "GOOGLE_API_KEY to your .env file for real questions."
            )

        else:

            st.warning(
                "Some questions fell back to placeholders because the "
                f"Gemini call failed: {questions.get('error')}"
            )

    if questions.get("skipped_skills"):

        st.info(
            "📚 No questions were generated for **" +
            ", ".join(questions["skipped_skills"]) +
            "** - you haven't ticked any resources for these skills as "
            "completed yet. Finish them on the 🗺️ Roadmap tab to have "
            "them included in your assessment."
        )

    st.subheader("MCQ Assessment")

    mcq_result = run_mcq_assessment(

        questions["mcq"]

    )

    st.divider()

    st.subheader("Coding Assessment")

    coding_result = run_coding_assessment(

        questions["coding"]

    )

    st.divider()

    if st.button(

        "Evaluate Assessment",

        use_container_width=True

    ):

        report = evaluate_assessment(

            mcq_result,

            coding_result

        )

        st.session_state.assessment_report = report

        save_state(

            user["id"],

            assessment_report=report,

            mcq_answers=st.session_state.get("mcq_answers", {}),

            coding_answers=st.session_state.get("coding_answers", {})

        )

        save_assessment(

            user["id"],

            report["mcq_score"],

            report["coding_score"],

            report["final_score"],

            report["grade"],

            report["performance"]

        )

        st.success(

            "Assessment Evaluated Successfully."

        )

        c1, c2, c3 = st.columns(3)

        c1.metric(

            "MCQ",

            f"{report['mcq_score']}%"

        )

        c2.metric(

            "Coding",

            f"{report['coding_score']}%"

        )

        c3.metric(

            "Final",

            f"{report['final_score']}%"

        )

        st.divider()

        st.subheader("Performance")

        st.success(

            report["performance"]

        )

        st.info(

            report["recommendation"]

        )

        st.divider()
# =========================================================
# FEEDBACK
# =========================================================

    if st.session_state.get(

        "assessment_report"

    ):

        st.divider()

        recommendation = run_feedback(

            st.session_state.assessment_report["final_score"]

        )

        if recommendation:

            st.session_state.feedback = recommendation

            raw_comments = st.session_state.get(
                "assessment_feedback", {}
            ).get("comments", "")

            # Log every submission to the feedback table (not just the
            # latest one in session state) so it can be reviewed later
            # from the Feedback tab or exported as CSV.
            save_feedback(

                user["id"],

                recommendation.get("difficulty"),

                None,

                None,

                recommendation.get("recommendation"),

                raw_comments

            )

            save_state(user["id"], feedback=recommendation)

            # Resources get re-ranked based on this feedback, so clear
            # previous selections - they were made against the old
            # ordering and may no longer be the right picks.
            for skill in list(st.session_state.selected_resources.keys()):

                for key in list(st.session_state.keys()):

                    if key.startswith(f"{skill}_"):

                        del st.session_state[key]

            st.session_state.selected_resources = {}

            save_state(user["id"], selected_resources={})

            adaptive_result = update_learning_plan(

                st.session_state.roadmap,

                st.session_state.assessment_report["final_score"],

                recommendation.get("difficulty", "Medium")

            )

            st.session_state.roadmap = adaptive_result["roadmap"]

            save_state(user["id"], roadmap=adaptive_result["roadmap"])

        if st.session_state.get("feedback"):

            st.divider()

            st.subheader("Updated Learning Plan")

            st.success(

                "Roadmap Updated Successfully."

            )

            st.info(
                f"📋 Your resource recommendations have been re-ranked "
                f"for a **{st.session_state.feedback.get('difficulty', 'Medium')}** "
                f"level based on your feedback."
            )

            if st.button("📚 View Updated Resources"):

                st.session_state.pending_nav = "📚 Resources"

                st.rerun()

# =========================================================
# ANALYTICS
# =========================================================

elif selected_page == "📈 Analytics":

    st.title("📈 Analytics Dashboard")

    if st.session_state.get("assessment_report") is None:

        st.warning(
            "Complete an assessment first."
        )

        st.stop()

    report = generate_report(

        current_user(),

        st.session_state.resume,

        st.session_state.job,

        st.session_state.skill_gap,

        st.session_state.roadmap,

        st.session_state.assessment_report,

        st.session_state.feedback

    )

    show_analytics(report)


# =========================================================
# REPORTS
# =========================================================

elif selected_page == "📑 Reports":

    st.title("📑 Final Report")

    if st.session_state.get("assessment_report") is None:

        st.warning(
            "No report available."
        )

        st.stop()

    report = generate_report(

        current_user(),

        st.session_state.resume,

        st.session_state.job,

        st.session_state.skill_gap,

        st.session_state.roadmap,

        st.session_state.assessment_report,

        st.session_state.feedback

    )

    st.success(
        "GapWise Report Generated Successfully"
    )

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        st.metric(

            "Skill Match",

            f"{report['skill_match']}%"

        )

    with c2:

        st.metric(

            "Assessment Score",

            f"{report['assessment_score']}%"

        )

    st.divider()

    st.subheader("Matched Skills")

    st.success(

        ", ".join(

            report["matched_skills"]

        )

    )

    st.subheader("Missing Skills")

    st.error(

        ", ".join(

            report["missing_skills"]

        )

    )

    st.divider()

    st.subheader("Roadmap Summary")

    for task in report["learning_plan"]:

        c1, c2, c3 = st.columns([4,1,1])

        with c1:

            st.write(task["skill"])

        with c2:

            st.write(task["status"])

        with c3:

            st.write(

                f"{task['progress']}%"

            )

    st.divider()

    st.subheader("Performance")

    st.info(

        report["performance"]

    )

    st.success(

        report["recommendation"]

    )

    st.divider()

    pdf_path = create_pdf(

        report

    )

    with open(

        pdf_path,

        "rb"

    ) as pdf:

        st.download_button(

            "📥 Download PDF Report",

            pdf,

            file_name="GapWise_Report.pdf",

            mime="application/pdf",

            use_container_width=True

        )

    st.divider()

    st.json(report)

# =========================================================
# FEEDBACK VIEWER (owner only)
# =========================================================

elif selected_page == "🗨️ Feedback":

    if not is_admin_user(user):

        st.error("You don't have access to this page.")

        st.stop()

    st.title("🗨️ User Feedback")

    st.write("Every feedback submission from every learner, newest first.")

    all_feedback = get_all_feedback()

    if not all_feedback:

        st.info("No feedback has been submitted yet.")

    else:

        import pandas as pd

        feedback_df = pd.DataFrame(all_feedback)

        st.metric("Total submissions", len(feedback_df))

        st.dataframe(
            feedback_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(

            "📥 Download Feedback as CSV",

            feedback_df.to_csv(index=False).encode("utf-8"),

            file_name="gapwise_feedback.csv",

            mime="text/csv",

            use_container_width=True

        )

# =========================================================
# FOOTER
# =========================================================

st.divider()

c1, c2, c3 = st.columns(3)

with c1:

    st.caption("GapWise AI")

with c2:

    st.caption(

        "Version 1.0"

    )

with c3:

    st.caption(

        f"© {datetime.now().year}"

    )