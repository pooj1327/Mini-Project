"""
config/config.py

Central Configuration for GapWise
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the project root regardless of the current working
# directory the app happens to be launched from.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


# ---------------------------------------------------
# Application
# ---------------------------------------------------

APP_NAME = "GapWise"

APP_VERSION = "1.0.0"

DEBUG = True


# ---------------------------------------------------
# API KEYS
# ---------------------------------------------------

GOOGLE_API_KEY = os.getenv(
    "GOOGLE_API_KEY",
    ""
)

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    ""
)

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    ""
)


# ---------------------------------------------------
# Database
# ---------------------------------------------------

DATABASE_PATH = "data/gapwise.db"


# ---------------------------------------------------
# Uploads
# ---------------------------------------------------

UPLOAD_FOLDER = "data/resumes"

REPORT_FOLDER = "data/reports"

TEST_FOLDER = "data/tests"

PROGRESS_FOLDER = "data/progress"


# ---------------------------------------------------
# Assessment
# ---------------------------------------------------

MCQ_PER_SKILL = 3

CODING_PER_SKILL = 1

PASSING_SCORE = 70


# ---------------------------------------------------
# Resume
# ---------------------------------------------------

MAX_UPLOAD_SIZE = 10

ALLOWED_FILES = [

    ".pdf",

    ".docx"

]


# ---------------------------------------------------
# LLM Settings
# ---------------------------------------------------

DEFAULT_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

TEMPERATURE = 0.3

MAX_TOKENS = 2048


# ---------------------------------------------------
# Skill Matching
# ---------------------------------------------------

SIMILARITY_THRESHOLD = 0.60


# ---------------------------------------------------
# Notifications
# ---------------------------------------------------

REMINDER_DAYS = 3


# ---------------------------------------------------
# Theme
# ---------------------------------------------------

PRIMARY_COLOR = "#4F46E5"

SECONDARY_COLOR = "#7C3AED"

SUCCESS_COLOR = "#16A34A"

ERROR_COLOR = "#DC2626"

WARNING_COLOR = "#F59E0B"


# ---------------------------------------------------
# Create Directories
# ---------------------------------------------------

for folder in [

    UPLOAD_FOLDER,

    REPORT_FOLDER,

    TEST_FOLDER,

    PROGRESS_FOLDER

]:

    os.makedirs(

        folder,

        exist_ok=True

    )