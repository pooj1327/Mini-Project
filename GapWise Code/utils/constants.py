"""
utils/constants.py

Application Constants
"""

APP_NAME = "GapWise AI"

APP_VERSION = "1.0.0"

APP_DESCRIPTION = (
    "Intelligent Skill Gap Detection "
    "with Human Feedback Loop"
)


# ---------------------------------------------
# Resume
# ---------------------------------------------

ALLOWED_RESUME_TYPES = [

    "pdf",

    "docx"

]

MAX_RESUME_SIZE_MB = 10


# ---------------------------------------------
# Assessment
# ---------------------------------------------

MCQ_PER_SKILL = 3

CODING_PER_SKILL = 1

PASSING_SCORE = 70


# ---------------------------------------------
# Progress
# ---------------------------------------------

ROADMAP_STATUS = [

    "Pending",

    "In Progress",

    "Completed"

]


# ---------------------------------------------
# Feedback Options
# ---------------------------------------------

FEEDBACK_OPTIONS = [

    "Easy",

    "Medium",

    "Hard"

]


# ---------------------------------------------
# Notification
# ---------------------------------------------

REMINDER_DAYS = 3


# ---------------------------------------------
# Database
# ---------------------------------------------

DATABASE_NAME = "gapwise.db"


# ---------------------------------------------
# Theme
# ---------------------------------------------

PRIMARY_COLOR = "#4F46E5"

SECONDARY_COLOR = "#6366F1"

SUCCESS_COLOR = "#16A34A"

WARNING_COLOR = "#F59E0B"

ERROR_COLOR = "#DC2626"


# ---------------------------------------------
# Charts
# ---------------------------------------------

CHART_HEIGHT = 400

PIE_HOLE = 0.5


# ---------------------------------------------
# Skill Matching
# ---------------------------------------------

SIMILARITY_THRESHOLD = 0.60


# ---------------------------------------------
# Session Keys
# ---------------------------------------------

SESSION_KEYS = [

    "user",

    "resume",

    "job",

    "skill_gap",

    "resources",

    "roadmap",

    "assessment",

    "feedback"

]