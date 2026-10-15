"""
dashboard/components.py

Reusable UI components for GapWise AI Dashboard
"""

import streamlit as st


def section_title(title: str, subtitle: str = ""):

    html = (
        '<div style="margin-bottom:10px;">'
        f'<h2 style="color:white;margin-bottom:0;">{title}</h2>'
        f'<p style="color:#94A3B8;margin-top:2px;">{subtitle}</p>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def metric_card(title, value, icon="📊", color="#7C3AED"):

    html = (
        '<div style="background:#1E293B;border-radius:18px;padding:20px;'
        'box-shadow:0 8px 20px rgba(0,0,0,.25);'
        f'border-left:5px solid {color};height:145px;">'
        f'<div style="font-size:30px;">{icon}</div>'
        f'<div style="color:#CBD5E1;margin-top:12px;font-size:15px;">{title}</div>'
        f'<div style="color:white;font-size:34px;font-weight:bold;margin-top:8px;">{value}</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def profile_card(name, email):

    avatar_name = name.replace(" ", "+")

    html = (
        '<div style="background:#1E293B;border-radius:18px;padding:20px;'
        'text-align:center;box-shadow:0 8px 20px rgba(0,0,0,.25);">'
        f'<img src="https://ui-avatars.com/api/?name={avatar_name}'
        '&background=7C3AED&color=fff&size=150" width="90" '
        'style="border-radius:50%;margin-bottom:15px;">'
        f'<h3 style="color:white;">{name}</h3>'
        f'<p style="color:#CBD5E1;">{email}</p>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def progress_card(skill, progress):

    st.markdown(f"**{skill}**")

    st.progress(progress / 100)

    st.caption(f"{progress}% Completed")


def notification_card(title, message):

    html = (
        '<div style="background:#312E81;padding:16px;'
        'border-radius:15px;margin-bottom:10px;">'
        f'<h4 style="color:white;margin-bottom:4px;">🔔 {title}</h4>'
        f'<p style="color:#E2E8F0;">{message}</p>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def roadmap_card(skill, status):

    emoji = "✅" if status else "⏳"

    color = "#22C55E" if status else "#F59E0B"

    html = (
        '<div style="background:#1E293B;padding:16px;'
        f'border-left:5px solid {color};border-radius:15px;margin-bottom:10px;">'
        f'<h4 style="color:white;">{emoji} {skill}</h4>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def assessment_card(title, score):

    html = (
        '<div style="background:#1E293B;border-radius:15px;padding:20px;">'
        f'<h4 style="color:white;">{title}</h4>'
        f'<h2 style="color:#22C55E;">{score}%</h2>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def resource_card(title, website, url):

    html = (
        '<div style="background:#1E293B;padding:18px;'
        'border-radius:15px;margin-bottom:10px;">'
        f'<h4 style="color:white;">{title}</h4>'
        f'<p style="color:#CBD5E1;">{website}</p>'
        f'<a href="{url}" target="_blank">Open Resource</a>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def divider():
    st.markdown("---")
