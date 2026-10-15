"""
database/state_db.py

Persists the in-progress application state for each user (resume,
job description, skill gap, selected resources, roadmap, assessment
questions/answers/report, feedback) so that everything is restored
automatically the next time the user logs back in - instead of being
lost the moment they log out (which only ever cleared Streamlit's
in-memory session_state, never touched the database).

Usage:

    from database.state_db import save_state, load_state

    save_state(user_id, resume=parsed_resume)
    saved = load_state(user_id)   # -> {"resume": {...}, "job": {...}, ...}
"""

import json

from database.database import db


# ----------------------------------------------------
# Table
# ----------------------------------------------------

STATE_FIELDS = [
    "resume",
    "job",
    "skill_gap",
    "selected_resources",
    "roadmap",
    "assessment_questions",
    "mcq_answers",
    "coding_answers",
    "assessment_report",
    "feedback",
]

_COLUMNS = [f"{field}_json" for field in STATE_FIELDS]

db.execute(
    f"""
    CREATE TABLE IF NOT EXISTS user_state(
        user_id INTEGER PRIMARY KEY,
        {", ".join(f"{col} TEXT" for col in _COLUMNS)},
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """
)


# ----------------------------------------------------
# Save (partial upsert - only touches the fields passed in)
# ----------------------------------------------------

def save_state(user_id, **fields):
    """
    Persist one or more pieces of state for a user.

    Only the keyword arguments actually passed are written - anything
    not passed is left exactly as it was already stored. Unknown
    field names are ignored rather than raising, so callers can pass
    through data safely.
    """

    fields = {
        key: value
        for key, value in fields.items()
        if key in STATE_FIELDS
    }

    if not fields:
        return

    columns = [f"{key}_json" for key in fields.keys()]
    values = [json.dumps(value) for value in fields.values()]

    existing = db.fetchone(
        "SELECT user_id FROM user_state WHERE user_id=?",
        (user_id,)
    )

    if existing:

        set_clause = ", ".join(f"{col}=?" for col in columns)

        db.execute(
            f"""
            UPDATE user_state
            SET {set_clause}, updated_at=CURRENT_TIMESTAMP
            WHERE user_id=?
            """,
            (*values, user_id)
        )

    else:

        all_columns = ["user_id"] + columns

        placeholders = ",".join("?" for _ in all_columns)

        db.execute(
            f"""
            INSERT INTO user_state({",".join(all_columns)})
            VALUES({placeholders})
            """,
            (user_id, *values)
        )


# ----------------------------------------------------
# Load
# ----------------------------------------------------

def load_state(user_id):
    """
    Returns a dict of every saved field for this user, decoded back
    into Python objects (dicts/lists/etc). Fields never saved, or
    saved as JSON null, are omitted from the result. Returns an
    empty dict if the user has no saved state at all.
    """

    row = db.fetchone(
        "SELECT * FROM user_state WHERE user_id=?",
        (user_id,)
    )

    if not row:
        return {}

    row = dict(row)

    result = {}

    for field in STATE_FIELDS:

        raw = row.get(f"{field}_json")

        if raw is None:
            continue

        try:
            value = json.loads(raw)
        except (TypeError, ValueError):
            continue

        if value is not None:
            result[field] = value

    return result


# ----------------------------------------------------
# Clear (used when a user explicitly wants to start over)
# ----------------------------------------------------

def clear_state(user_id):

    db.execute(
        "DELETE FROM user_state WHERE user_id=?",
        (user_id,)
    )
