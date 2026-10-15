"""
utils/helpers.py

Common helper functions used across the application.
"""

import os
import uuid
import json
from datetime import datetime


# --------------------------------------------------
# Timestamp
# --------------------------------------------------

def current_timestamp():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# --------------------------------------------------
# Date
# --------------------------------------------------

def current_date():

    return datetime.now().strftime(
        "%Y-%m-%d"
    )


# --------------------------------------------------
# Generate Unique ID
# --------------------------------------------------

def generate_id():

    return str(uuid.uuid4())


# --------------------------------------------------
# Save JSON
# --------------------------------------------------

def save_json(filepath, data):

    with open(filepath, "w", encoding="utf-8") as file:

        json.dump(

            data,

            file,

            indent=4

        )


# --------------------------------------------------
# Load JSON
# --------------------------------------------------

def load_json(filepath):

    if not os.path.exists(filepath):

        return {}

    with open(filepath, "r", encoding="utf-8") as file:

        return json.load(file)


# --------------------------------------------------
# Create Directory
# --------------------------------------------------

def create_directory(path):

    os.makedirs(

        path,

        exist_ok=True

    )


# --------------------------------------------------
# Format Skills
# --------------------------------------------------

def format_skills(skills):

    if isinstance(skills, str):

        skills = skills.split(",")

    return [

        skill.strip()

        for skill in skills

        if skill.strip()

    ]


# --------------------------------------------------
# Convert List to String
# --------------------------------------------------

def skills_to_string(skills):

    return ", ".join(skills)


# --------------------------------------------------
# Percentage
# --------------------------------------------------

def percentage(part, total):

    if total == 0:

        return 0

    return round(

        (part / total) * 100,

        2

    )


# --------------------------------------------------
# Progress Color
# --------------------------------------------------

def progress_color(progress):

    if progress >= 80:

        return "green"

    elif progress >= 50:

        return "orange"

    return "red"


# --------------------------------------------------
# Greeting
# --------------------------------------------------

def greeting():

    hour = datetime.now().hour

    if hour < 12:

        return "Good Morning"

    elif hour < 17:

        return "Good Afternoon"

    return "Good Evening"


# --------------------------------------------------
# Truncate Text
# --------------------------------------------------

def truncate(text, length=100):

    if len(text) <= length:

        return text

    return text[:length] + "..."


# --------------------------------------------------
# Deadline Remaining
# --------------------------------------------------

def days_remaining(deadline):

    if isinstance(deadline, str):

        deadline = datetime.strptime(

            deadline,

            "%Y-%m-%d"

        )

    today = datetime.today()

    days = (

        deadline - today

    ).days

    return max(days, 0)


# --------------------------------------------------
# Skill Level
# --------------------------------------------------

def skill_level(score):

    if score >= 90:

        return "Expert"

    elif score >= 75:

        return "Advanced"

    elif score >= 60:

        return "Intermediate"

    return "Beginner"


# --------------------------------------------------
# Empty Check
# --------------------------------------------------

def is_empty(value):

    if value is None:

        return True

    if isinstance(value, str):

        return len(value.strip()) == 0

    if isinstance(value, list):

        return len(value) == 0

    return False


# --------------------------------------------------
# Safe Integer
# --------------------------------------------------

def to_int(value, default=0):

    try:

        return int(value)

    except Exception:

        return default


# --------------------------------------------------
# Safe Float
# --------------------------------------------------

def to_float(value, default=0.0):

    try:

        return float(value)

    except Exception:

        return default