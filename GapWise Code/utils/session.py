"""
utils/session.py

Session State Manager for GapWise
"""

import streamlit as st


# --------------------------------------------------
# Initialize Session
# --------------------------------------------------

def initialize_session():

    defaults = {

        "logged_in": False,

        "user": None,

        "resume": None,

        "job": None,

        "skill_gap": None,

        "selected_resources": {},

        "roadmap": [],

        "roadmap_progress": [],

        "assessment_questions": [],

        "mcq_answers": {},

        "coding_answers": {},

        "mcq_report": None,

        "coding_report": None,

        "assessment_report": None,

        "feedback": None,

        "notifications": [],

        "theme": "light"

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# --------------------------------------------------
# Login
# --------------------------------------------------

def login(user):

    st.session_state.logged_in = True

    st.session_state.user = user


# --------------------------------------------------
# Logout
# --------------------------------------------------

def logout():

    keys = list(st.session_state.keys())

    for key in keys:

        del st.session_state[key]

    initialize_session()


# --------------------------------------------------
# User
# --------------------------------------------------

def current_user():

    return st.session_state.get("user")


def is_logged_in():

    return st.session_state.get(

        "logged_in",

        False

    )


# --------------------------------------------------
# Resume
# --------------------------------------------------

def set_resume(resume):

    st.session_state.resume = resume


def get_resume():

    return st.session_state.resume


# --------------------------------------------------
# Job Description
# --------------------------------------------------

def set_job(job):

    st.session_state.job = job


def get_job():

    return st.session_state.job


# --------------------------------------------------
# Skill Gap
# --------------------------------------------------

def set_skill_gap(result):

    st.session_state.skill_gap = result


def get_skill_gap():

    return st.session_state.skill_gap


# --------------------------------------------------
# Resources
# --------------------------------------------------

def set_resources(resources):

    st.session_state.selected_resources = resources


def get_resources():

    return st.session_state.selected_resources


# --------------------------------------------------
# Roadmap
# --------------------------------------------------

def set_roadmap(roadmap):

    st.session_state.roadmap = roadmap


def get_roadmap():

    return st.session_state.roadmap


# --------------------------------------------------
# Assessment
# --------------------------------------------------

def set_assessment(report):

    st.session_state.assessment_report = report


def get_assessment():

    return st.session_state.assessment_report


# --------------------------------------------------
# Feedback
# --------------------------------------------------

def set_feedback(feedback):

    st.session_state.feedback = feedback


def get_feedback():

    return st.session_state.feedback


# --------------------------------------------------
# Notifications
# --------------------------------------------------

def add_notification(message):

    st.session_state.notifications.append(message)


def get_notifications():

    return st.session_state.notifications


def clear_notifications():

    st.session_state.notifications = []


# --------------------------------------------------
# Theme
# --------------------------------------------------

def set_theme(theme):

    st.session_state.theme = theme


def get_theme():

    return st.session_state.theme


# --------------------------------------------------
# Reset Workflow
# --------------------------------------------------

def reset_workflow():

    st.session_state.resume = None

    st.session_state.job = None

    st.session_state.skill_gap = None

    st.session_state.selected_resources = {}

    st.session_state.roadmap = []

    st.session_state.roadmap_progress = []

    st.session_state.assessment_questions = []

    st.session_state.mcq_answers = {}

    st.session_state.coding_answers = {}

    st.session_state.assessment_report = None

    st.session_state.feedback = None

    st.session_state.notifications = []


# --------------------------------------------------
# Completion Check
# --------------------------------------------------

def workflow_completed():

    return (

        st.session_state.resume is not None and

        st.session_state.job is not None and

        st.session_state.skill_gap is not None and

        len(st.session_state.roadmap) > 0 and

        st.session_state.assessment_report is not None

    )