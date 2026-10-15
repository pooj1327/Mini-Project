"""
database/roadmap_db.py

Database operations for Learning Roadmap
"""

import json

from database.database import db


# ----------------------------------------------------
# Save Roadmap
# ----------------------------------------------------

def save_roadmap(
    user_id,
    roadmap
):

    db.execute(

        """

        DELETE FROM roadmap

        WHERE user_id=?

        """,

        (user_id,)

    )

    for item in roadmap:

        db.execute(

            """

            INSERT INTO roadmap(

                user_id,

                skill,

                status,

                progress,

                completed,

                start_date,

                end_date

            )

            VALUES(?,?,?,?,?,?,?)

            """,

            (

                user_id,

                item["skill"],

                item["status"],

                item["progress"],

                int(item["completed"]),

                item["start_date"],

                item["end_date"]

            )

        )


# ----------------------------------------------------
# Get Roadmap
# ----------------------------------------------------

def get_roadmap(user_id):

    rows = db.fetchall(

        """

        SELECT *

        FROM roadmap

        WHERE user_id=?

        ORDER BY id

        """,

        (user_id,)

    )

    roadmap = []

    for row in rows:

        roadmap.append({

            "id": row["id"],

            "skill": row["skill"],

            "status": row["status"],

            "progress": row["progress"],

            "completed": bool(row["completed"]),

            "start_date": row["start_date"],

            "end_date": row["end_date"]

        })

    return roadmap


# ----------------------------------------------------
# Update Progress
# ----------------------------------------------------

def update_progress(
    roadmap_id,
    progress
):

    status = "Pending"

    completed = 0

    if progress >= 100:

        progress = 100

        status = "Completed"

        completed = 1

    elif progress > 0:

        status = "In Progress"

    db.execute(

        """

        UPDATE roadmap

        SET

            progress=?,

            status=?,

            completed=?

        WHERE id=?

        """,

        (

            progress,

            status,

            completed,

            roadmap_id

        )

    )


# ----------------------------------------------------
# Mark Completed
# ----------------------------------------------------

def mark_completed(
    roadmap_id
):

    db.execute(

        """

        UPDATE roadmap

        SET

            progress=100,

            status='Completed',

            completed=1

        WHERE id=?

        """,

        (roadmap_id,)

    )


# ----------------------------------------------------
# Delete Roadmap
# ----------------------------------------------------

def delete_roadmap(
    user_id
):

    db.execute(

        """

        DELETE FROM roadmap

        WHERE user_id=?

        """,

        (user_id,)

    )


# ----------------------------------------------------
# Overall Progress
# ----------------------------------------------------

def overall_progress(
    user_id
):

    rows = get_roadmap(user_id)

    if len(rows) == 0:

        return 0

    total = sum(

        row["progress"]

        for row in rows

    )

    return round(

        total / len(rows),

        2

    )


# ----------------------------------------------------
# Completed Skills
# ----------------------------------------------------

def completed_skills(
    user_id
):

    rows = get_roadmap(user_id)

    return len(

        [

            r

            for r in rows

            if r["completed"]

        ]

    )


# ----------------------------------------------------
# Pending Skills
# ----------------------------------------------------

def pending_skills(
    user_id
):

    rows = get_roadmap(user_id)

    return len(

        [

            r

            for r in rows

            if not r["completed"]

        ]

    )