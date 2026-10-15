"""
database/progress_db.py

Database operations for User Progress Tracking
"""

from database.database import db


# ----------------------------------------------------
# Save Progress
# ----------------------------------------------------

def save_progress(
    user_id,
    overall_progress
):

    existing = db.fetchone(

        """

        SELECT *

        FROM progress

        WHERE user_id=?

        """,

        (user_id,)

    )

    if existing:

        db.execute(

            """

            UPDATE progress

            SET overall_progress=?

            WHERE user_id=?

            """,

            (

                overall_progress,

                user_id

            )

        )

    else:

        db.execute(

            """

            INSERT INTO progress(

                user_id,

                overall_progress

            )

            VALUES(?,?)

            """,

            (

                user_id,

                overall_progress

            )

        )


# ----------------------------------------------------
# Get Progress
# ----------------------------------------------------

def get_progress(user_id):

    row = db.fetchone(

        """

        SELECT *

        FROM progress

        WHERE user_id=?

        """,

        (user_id,)

    )

    if row:

        return dict(row)

    return None


# ----------------------------------------------------
# Update Progress
# ----------------------------------------------------

def update_progress(
    user_id,
    progress
):

    save_progress(
        user_id,
        progress
    )


# ----------------------------------------------------
# Reset Progress
# ----------------------------------------------------

def reset_progress(user_id):

    db.execute(

        """

        UPDATE progress

        SET overall_progress=0

        WHERE user_id=?

        """,

        (user_id,)

    )


# ----------------------------------------------------
# Delete Progress
# ----------------------------------------------------

def delete_progress(user_id):

    db.execute(

        """

        DELETE FROM progress

        WHERE user_id=?

        """,

        (user_id,)

    )


# ----------------------------------------------------
# Check Completion
# ----------------------------------------------------

def is_completed(user_id):

    progress = get_progress(user_id)

    if not progress:

        return False

    return progress["overall_progress"] >= 100


# ----------------------------------------------------
# Dashboard Summary
# ----------------------------------------------------

def dashboard_progress(user_id):

    progress = get_progress(user_id)

    if not progress:

        return {

            "overall_progress": 0,

            "status": "Not Started"

        }

    value = progress["overall_progress"]

    if value == 100:

        status = "Completed"

    elif value > 0:

        status = "In Progress"

    else:

        status = "Not Started"

    return {

        "overall_progress": value,

        "status": status

    }