"""
database/assessment_db.py

Database operations for Assessment Results
"""

from database.database import db


# ----------------------------------------------------
# Save Assessment
# ----------------------------------------------------

def save_assessment(
    user_id,
    mcq_score,
    coding_score,
    final_score,
    grade,
    performance
):

    db.execute(

        """

        INSERT INTO assessments(

            user_id,

            mcq_score,

            coding_score,

            final_score,

            grade,

            performance

        )

        VALUES(?,?,?,?,?,?)

        """,

        (

            user_id,

            mcq_score,

            coding_score,

            final_score,

            grade,

            performance

        )

    )


# ----------------------------------------------------
# Get Latest Assessment
# ----------------------------------------------------

def get_latest_assessment(user_id):

    row = db.fetchone(

        """

        SELECT *

        FROM assessments

        WHERE user_id=?

        ORDER BY assessment_date DESC

        LIMIT 1

        """,

        (user_id,)

    )

    if row:

        return dict(row)

    return None


# ----------------------------------------------------
# Get All Assessments
# ----------------------------------------------------

def get_all_assessments(user_id):

    rows = db.fetchall(

        """

        SELECT *

        FROM assessments

        WHERE user_id=?

        ORDER BY assessment_date DESC

        """,

        (user_id,)

    )

    return [

        dict(row)

        for row in rows

    ]


# ----------------------------------------------------
# Delete Assessment
# ----------------------------------------------------

def delete_assessment(assessment_id):

    db.execute(

        """

        DELETE FROM assessments

        WHERE id=?

        """,

        (assessment_id,)

    )


# ----------------------------------------------------
# Average Score
# ----------------------------------------------------

def average_score(user_id):

    rows = get_all_assessments(user_id)

    if len(rows) == 0:

        return 0

    total = sum(

        row["final_score"]

        for row in rows

    )

    return round(

        total / len(rows),

        2

    )


# ----------------------------------------------------
# Highest Score
# ----------------------------------------------------

def highest_score(user_id):

    rows = get_all_assessments(user_id)

    if len(rows) == 0:

        return 0

    return max(

        row["final_score"]

        for row in rows

    )


# ----------------------------------------------------
# Total Attempts
# ----------------------------------------------------

def total_attempts(user_id):

    return len(

        get_all_assessments(user_id)

    )


# ----------------------------------------------------
# Save Feedback
# ----------------------------------------------------

def save_feedback(

    user_id,

    difficulty,

    confidence,

    satisfaction,

    recommendation,

    comments

):

    db.execute(

        """

        INSERT INTO feedback(

            user_id,

            difficulty,

            confidence,

            satisfaction,

            recommendation,

            comments

        )

        VALUES(?,?,?,?,?,?)

        """,

        (

            user_id,

            difficulty,

            confidence,

            satisfaction,

            recommendation,

            comments

        )

    )


# ----------------------------------------------------
# Get Latest Feedback
# ----------------------------------------------------

def latest_feedback(user_id):

    row = db.fetchone(

        """

        SELECT *

        FROM feedback

        WHERE user_id=?

        ORDER BY created_at DESC

        LIMIT 1

        """,

        (user_id,)

    )

    if row:

        return dict(row)

    return None


# ----------------------------------------------------
# Get All Feedback (across every user - for the in-app
# feedback viewer / CSV export)
# ----------------------------------------------------

def get_all_feedback():

    rows = db.fetchall(

        """

        SELECT

            feedback.id,

            feedback.user_id,

            users.name AS user_name,

            users.email AS user_email,

            feedback.difficulty,

            feedback.confidence,

            feedback.satisfaction,

            feedback.recommendation,

            feedback.comments,

            feedback.created_at

        FROM feedback

        LEFT JOIN users
            ON users.id = feedback.user_id

        ORDER BY feedback.created_at DESC

        """

    )

    return [
        dict(row)
        for row in rows
    ]


# ----------------------------------------------------
# Assessment Statistics
# ----------------------------------------------------

def assessment_statistics(user_id):

    return {

        "attempts": total_attempts(user_id),

        "average_score": average_score(user_id),

        "highest_score": highest_score(user_id),

        "latest_feedback": latest_feedback(user_id)

    }