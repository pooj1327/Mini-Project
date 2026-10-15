"""
resources/resource_selector.py

Allows the user to select learning resources for each missing skill.
Stores the selected resources in Streamlit Session State.
"""

import streamlit as st

from dashboard.theme import resource_card, inject_theme_css


def initialize_resource_session():

    if "selected_resources" not in st.session_state:
        st.session_state.selected_resources = {}


def display_resources(resource_plan):
    """
    Display resources with checkboxes, grouped into a collapsible
    section per skill (so you're not scrolling through every skill's
    resources at once) with a compact 2-column grid inside.
    """

    inject_theme_css()

    initialize_resource_session()

    st.title("📚 Learning Resources")

    if not resource_plan:

        st.success("No missing skills detected!")

        return {}

    skills = list(resource_plan.items())

    for position, (skill, resources) in enumerate(skills):

        previously_selected_urls = {
            r["url"] for r in st.session_state.selected_resources.get(skill, [])
        }

        selected_count = len(previously_selected_urls)

        header = f"🔹 {skill}  ·  {len(resources)} resources"

        if selected_count:
            header += f"  ·  ✅ {selected_count} selected"

        with st.expander(header, expanded=(position == 0)):

            selected = []

            cols = st.columns(2)

            for index, resource in enumerate(resources):

                with cols[index % 2]:

                    resource_card(
                        title=resource["title"],
                        platform=resource["platform"],
                        subtitle=resource["platform"],
                        url=resource["url"],
                        best_pick=(index == 0)
                    )

                    check = st.checkbox(
                        "Select this resource",
                        key=f"{skill}_{index}",
                        value=resource["url"] in previously_selected_urls
                    )

                if check:
                    selected.append(resource)

            st.session_state.selected_resources[skill] = selected

    return st.session_state.selected_resources


def get_selected_resources():

    initialize_resource_session()

    return st.session_state.selected_resources


def selected_resource_count():

    initialize_resource_session()

    count = 0

    for skill in st.session_state.selected_resources:

        count += len(
            st.session_state.selected_resources[skill]
        )

    return count


def selected_skills():

    initialize_resource_session()

    skills = []

    for skill, resources in st.session_state.selected_resources.items():

        if len(resources) > 0:

            skills.append(skill)

    return skills


def clear_selected_resources():

    st.session_state.selected_resources = {}