"""
dashboard/sidebar.py

Professional Sidebar Navigation for GapWise AI
"""

import streamlit as st
from streamlit_option_menu import option_menu


def sidebar(user_name="User"):
    """
    Render Sidebar Navigation
    Returns selected menu item.
    """

    with st.sidebar:

        st.markdown(
            """
            <div style='text-align:center;padding:10px'>
                <h1 style='color:#7C3AED;'>🎯 GapWise AI</h1>
                <p style='color:gray;'>Skill Gap Detection Platform</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        st.markdown(
            f"""
            <div style='text-align:center;'>

            <img src="https://ui-avatars.com/api/?name={user_name}&background=7C3AED&color=fff&size=200"
            width="90"
            style="border-radius:50%;">

            <h3 style='margin-top:10px;'>{user_name}</h3>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        selected = option_menu(
            menu_title=None,

            options=[
                "Dashboard",
                "Resume",
                "Job Description",
                "Skill Gap",
                "Resources",
                "Roadmap",
                "Progress",
                "Assessment",
                "Reports",
                "Settings",
                "Logout"
            ],

            icons=[
                "speedometer2",
                "file-earmark-person",
                "briefcase",
                "bar-chart",
                "book",
                "map",
                "graph-up-arrow",
                "clipboard-check",
                "file-earmark-pdf",
                "gear",
                "box-arrow-right"
            ],

            menu_icon="cast",

            default_index=0,

            styles={
                "container": {
                    "padding": "5px",
                    "background-color": "#111827",
                },

                "icon": {
                    "color": "#7C3AED",
                    "font-size": "18px",
                },

                "nav-link": {
                    "font-size": "15px",
                    "text-align": "left",
                    "margin": "5px",
                    "--hover-color": "#1E293B",
                    "border-radius": "10px",
                },

                "nav-link-selected": {
                    "background-color": "#7C3AED",
                    "color": "white",
                    "font-weight": "bold",
                },
            },
        )

        st.markdown("---")

        st.caption("GapWise AI v1.0")
       