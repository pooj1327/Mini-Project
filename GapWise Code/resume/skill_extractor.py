"""
resume/skill_extractor.py

Extract Name, Email, Phone and Skills from Resume Text.
"""

import re
import spacy


_nlp = None
_nlp_load_attempted = False


def _get_nlp():
    """
    Lazily load the spacy model, and never crash the app if it's
    missing. `pip install spacy` alone does not install the
    'en_core_web_sm' model - it needs a separate download
    (`python -m spacy download en_core_web_sm`). If it isn't
    available, name extraction falls back to a simple heuristic
    instead of taking down the whole app.
    """

    global _nlp, _nlp_load_attempted

    if _nlp_load_attempted:
        return _nlp

    _nlp_load_attempted = True

    try:
        _nlp = spacy.load("en_core_web_sm")
    except Exception:
        _nlp = None

    return _nlp


# Skill vocabulary now lives in utils/skills_db.py so that resume
# parsing and job-description parsing match against the SAME list.
# They previously had separate, shorter copies, which produced false
# "missing skills" whenever the two lists disagreed.

from utils.skills_db import SKILL_DATABASE, canonical_skill

# --------------------------------------------------
# Email
# --------------------------------------------------

def extract_email(text):

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    result = re.findall(pattern, text)

    return result[0] if result else ""


# --------------------------------------------------
# Phone
# --------------------------------------------------

def extract_phone(text):

    pattern = r'(\+?\d[\d\s\-]{8,15})'

    result = re.findall(pattern, text)

    return result[0] if result else ""


# --------------------------------------------------
# Name
# --------------------------------------------------

NAME_STOPWORDS = {
    "resume", "curriculum vitae", "cv", "bio-data", "biodata",
    "profile", "summary", "contact", "objective", "career objective",
    "professional summary", "profile summary", "personal details",
    "education", "experience", "work experience",
    "professional experience", "skills", "technical skills",
    "soft skills", "projects", "certifications", "achievements",
    "declaration", "references", "languages known", "hobbies",
    "interests", "about me", "contact information", "personal information"
}

# A plausible "Full Name" line: 2-4 words, each starting with a
# capital letter (or the whole word in caps), letters/periods/
# hyphens/apostrophes only - no digits or stray punctuation.
_NAME_PATTERN = re.compile(
    r"^[A-Z][a-zA-Z.'-]*(\s+[A-Z][a-zA-Z.'-]*){1,3}$"
)


def _clean_candidate_line(line):
    """
    Strips common resume-header noise from a line before it's
    checked as a name candidate: leading bullets/emoji, and
    anything after a '|' or '-' separator (e.g. job titles
    tacked onto the same line as the name).
    """

    line = line.strip()

    # Drop common leading bullet/icon characters
    line = re.sub(r"^[•\-\*\u2022\u25CF\u25A0>]+\s*", "", line)

    # If the line has a separator, the name is usually the first segment
    for sep in ["|", "•", "–", "—"]:
        if sep in line:
            line = line.split(sep)[0].strip()
            break

    return line


def extract_name(text, name_hint=None):

    if name_hint:

        cleaned_hint = _clean_candidate_line(name_hint)

        if cleaned_hint and cleaned_hint.lower() not in NAME_STOPWORDS and "@" not in cleaned_hint:

            return cleaned_hint

    nlp = _get_nlp()

    if nlp is not None:

        doc = nlp(text)

        for ent in doc.ents:

            if ent.label_ == "PERSON":

                return ent.text

    raw_lines = [line.strip() for line in text.split("\n")]

    candidates = []

    for line in raw_lines[:15]:

        if not line:
            continue

        cleaned = _clean_candidate_line(line)

        if not cleaned:
            continue

        lowered = cleaned.lower()

        if lowered in NAME_STOPWORDS:
            continue

        if "@" in cleaned:
            continue

        if re.search(r"\d", cleaned):
            continue

        if len(cleaned) > 40:
            continue

        candidates.append(cleaned)

    # Pass 1: prefer a line that actually looks like "Firstname Lastname"
    for cleaned in candidates:

        title_cased = " ".join(w.capitalize() for w in cleaned.split())

        if _NAME_PATTERN.match(cleaned) or _NAME_PATTERN.match(title_cased):

            return title_cased if cleaned.isupper() else cleaned

    # Pass 2: fall back to the first reasonable-looking line
    for cleaned in candidates:

        if len(cleaned.split()) <= 5:
            return cleaned

    return raw_lines[0].strip() if raw_lines else ""


# --------------------------------------------------
# Skills
# --------------------------------------------------

def extract_skills(text):

    text_lower = text.lower()

    found = set()

    for skill in SKILL_DATABASE:

        pattern = r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9+#])"

        if re.search(pattern, text_lower):

            # Normalise to the canonical name so "sklearn" and
            # "scikit-learn" collapse into one skill instead of
            # appearing as two separate ones.
            found.add(canonical_skill(skill) or skill.title())

    return sorted(found)


# --------------------------------------------------
# Complete Extraction
# --------------------------------------------------

def extract_resume_details(text, name_hint=None):

    return {

        "name": extract_name(text, name_hint=name_hint),

        "email": extract_email(text),

        "phone": extract_phone(text),

        "skills": extract_skills(text)
    }