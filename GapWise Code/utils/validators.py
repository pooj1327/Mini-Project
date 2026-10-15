"""
utils/validators.py

Validation functions used throughout GapWise.
"""

import re
from pathlib import Path


# --------------------------------------------------
# Name Validation
# --------------------------------------------------

def validate_name(name):

    if not name:
        return False

    name = name.strip()

    if len(name) < 2:
        return False

    return True


# --------------------------------------------------
# Email Validation
# --------------------------------------------------

def validate_email(email):

    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    return bool(
        re.match(pattern, email)
    )


# --------------------------------------------------
# Password Validation
# --------------------------------------------------

def validate_password(password):

    if len(password) < 8:

        return False

    if not re.search(r"[A-Z]", password):

        return False

    if not re.search(r"[a-z]", password):

        return False

    if not re.search(r"\d", password):

        return False

    if not re.search(r"[!@#$%^&*()_+=\-{}[\]:;\"'<>,.?/\\|]", password):

        return False

    return True


# --------------------------------------------------
# Phone Number
# --------------------------------------------------

def validate_phone(phone):

    pattern = r'^[6-9]\d{9}$'

    return bool(
        re.match(pattern, phone)
    )


# --------------------------------------------------
# Resume File Validation
# --------------------------------------------------

def validate_resume(file):

    if file is None:

        return False

    extension = Path(
        file.name
    ).suffix.lower()

    return extension in [

        ".pdf",

        ".docx"

    ]


# --------------------------------------------------
# Job Description
# --------------------------------------------------

def validate_job_description(text):

    if text is None:

        return False

    if len(text.strip()) < 100:

        return False

    return True


# --------------------------------------------------
# Skills
# --------------------------------------------------

def validate_skills(skills):

    if len(skills) == 0:

        return False

    return True


# --------------------------------------------------
# Deadline
# --------------------------------------------------

def validate_deadline(deadline):

    return deadline is not None


# --------------------------------------------------
# Assessment Answers
# --------------------------------------------------

def validate_answers(answers):

    if len(answers) == 0:

        return False

    for answer in answers:

        if answer == "":

            return False

    return True


# --------------------------------------------------
# Feedback
# --------------------------------------------------

def validate_feedback(feedback):

    if feedback is None:

        return False

    if len(feedback.strip()) == 0:

        return False

    return True


# --------------------------------------------------
# URL
# --------------------------------------------------

def validate_url(url):

    pattern = (

        r'^(http|https)://'

        r'([A-Za-z0-9.-]+)'

        r'(\.[A-Za-z]{2,})'

        r'(/[A-Za-z0-9._/?=&%-]*)?$'

    )

    return bool(

        re.match(pattern, url)

    )