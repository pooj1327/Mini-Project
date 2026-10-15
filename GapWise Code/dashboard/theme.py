"""
dashboard/theme.py

Shared color palette and global CSS for the GapWise AI dashboard.
"""

import textwrap

import streamlit as st


# ---------------------------------------------------------
# Palette
# ---------------------------------------------------------

BG = "#0B1120"
SURFACE = "#151B2E"
CARD = "#1E293B"
BORDER = "#243049"

PRIMARY = "#7C3AED"
BLUE = "#2563EB"
GREEN = "#22C55E"
ORANGE = "#F59E0B"
RED = "#EF4444"
PINK = "#EC4899"

TEXT = "#F1F5F9"
MUTED = "#94A3B8"


def inject_theme_css():
    """
    Injects the global dark / purple theme once per page load.
    Safe to call on every page - Streamlit just re-applies the same CSS.
    """

    css = textwrap.dedent(f"""
    <style>
    .stApp {{
        background-color: {BG};
    }}
    section[data-testid="stSidebar"] {{
        background-color: {SURFACE};
        border-right: 1px solid {BORDER};
    }}
    h1, h2, h3, h4, h5, h6, p, span, label, li {{
        color: {TEXT};
    }}
    [data-testid="stMetric"] {{
        background-color: {CARD};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 16px 18px;
    }}
    [data-testid="stMetricLabel"] {{
        color: {MUTED};
    }}
    .stButton > button {{
        background-color: {PRIMARY};
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 16px;
        font-weight: 600;
    }}
    .stButton > button:hover {{
        background-color: #6D28D9;
        color: white;
    }}
    div[data-baseweb="tab-list"] {{
        gap: 6px;
    }}
    hr {{
        border-color: {BORDER};
    }}
    </style>
    """)

    st.markdown(css, unsafe_allow_html=True)


KPI_GRADIENTS = {
    "#7C3AED": "linear-gradient(135deg,#6D28D9,#8B5CF6)",
    "#22C55E": "linear-gradient(135deg,#15803D,#22C55E)",
    "#2563EB": "linear-gradient(135deg,#1D4ED8,#3B82F6)",
    "#F59E0B": "linear-gradient(135deg,#B45309,#F59E0B)",
    "#EC4899": "linear-gradient(135deg,#BE185D,#EC4899)",
}


def kpi_card(label, value, sublabel="", icon="📊", color=PRIMARY):
    """
    Colored gradient KPI card matching the dashboard mockup
    (icon badge + big number + label + optional sublabel).
    """

    gradient = KPI_GRADIENTS.get(color, f"linear-gradient(135deg,{color},{color})")

    sublabel_html = (
        f'<div style="color:rgba(255,255,255,.7);font-size:11px;margin-top:4px;">{sublabel}</div>'
        if sublabel else ""
    )

    html = (
        f'<div style="background:{gradient};'
        f'border-radius:16px;padding:16px 18px;min-height:110px;'
        f'box-shadow:0 6px 16px rgba(0,0,0,.25);">'
        f'<div style="font-size:20px;margin-bottom:8px;">{icon}</div>'
        f'<div style="color:white;font-size:26px;font-weight:700;">{value}</div>'
        f'<div style="color:rgba(255,255,255,.85);font-size:13px;margin-top:2px;">{label}</div>'
        f'{sublabel_html}'
        f'</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


PLATFORM_STYLE = {
    "YouTube": {"icon": "▶️", "bg": "#FF0000", "action": "Watch"},
    "freeCodeCamp": {"icon": "🟢", "bg": "#0A0A23", "action": "Visit"},
    "Coursera": {"icon": "🎓", "bg": "#0056D2", "action": "View"},
    "edX": {"icon": "📘", "bg": "#02262B", "action": "View"},
    "Udemy": {"icon": "🅄", "bg": "#7C3AED", "action": "View"},
    "GeeksforGeeks": {"icon": "🟩", "bg": "#2F8D46", "action": "Visit"},
    "W3Schools": {"icon": "🌐", "bg": "#04AA6D", "action": "Visit"},
    "Official Docs": {"icon": "📄", "bg": "#2563EB", "action": "Visit"},
}

DEFAULT_PLATFORM_STYLE = {"icon": "🔗", "bg": "#475569", "action": "Open"}


def resource_card(title, platform, subtitle, url, best_pick=False):
    """
    Resource card: colored platform badge + title/subtitle + an
    action button that opens the resource in a new tab. Optionally
    shows a "Best Pick" badge for the top recommended resource.
    """

    style = PLATFORM_STYLE.get(platform, DEFAULT_PLATFORM_STYLE)

    badge_html = (
        '<span style="background:#F59E0B22;color:#F59E0B;font-size:11px;'
        'font-weight:700;padding:3px 8px;border-radius:20px;margin-left:8px;">'
        '⭐ Best Pick</span>'
        if best_pick else ''
    )

    border = '2px solid #F59E0B' if best_pick else '1px solid #243049'

    html = (
        f'<div style="background:#1E293B;border:{border};'
        'border-radius:14px;padding:14px 16px;margin-bottom:10px;'
        'display:flex;align-items:center;justify-content:space-between;gap:12px;">'
        '<div style="display:flex;align-items:center;gap:12px;min-width:0;">'
        f'<div style="width:38px;height:38px;flex-shrink:0;border-radius:10px;'
        f'background:{style["bg"]};display:flex;align-items:center;'
        f'justify-content:center;font-size:16px;">{style["icon"]}</div>'
        '<div style="min-width:0;">'
        f'<div style="color:#F1F5F9;font-weight:600;font-size:14px;'
        f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{title}{badge_html}</div>'
        f'<div style="color:#94A3B8;font-size:12px;">{subtitle}</div>'
        '</div>'
        '</div>'
        f'<a href="{url}" target="_blank" style="flex-shrink:0;'
        f'background:#7C3AED;color:white;text-decoration:none;'
        f'font-size:13px;font-weight:600;padding:8px 16px;border-radius:10px;">'
        f'{style["action"]}</a>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)




def task_row(title, subtitle, status):
    """
    Single row for the "Upcoming Tasks" list.
    """

    status_colors = {
        "Completed": GREEN,
        "In Progress": BLUE,
        "Pending": ORANGE,
        "Not Started": MUTED,
    }

    color = status_colors.get(status, MUTED)

    html = (
        f'<div style="background:{CARD};border:1px solid {BORDER};'
        f'border-radius:12px;padding:12px 14px;margin-bottom:8px;'
        f'display:flex;justify-content:space-between;align-items:center;">'
        f'<div>'
        f'<div style="color:{TEXT};font-weight:600;font-size:14px;">{title}</div>'
        f'<div style="color:{MUTED};font-size:12px;">{subtitle}</div>'
        f'</div>'
        f'<div style="color:{color};font-size:12px;font-weight:600;'
        f'background:{color}22;padding:4px 10px;border-radius:20px;">'
        f'{status}</div>'
        f'</div>'
    )

    st.markdown(html, unsafe_allow_html=True)
