"""
database/auth_db.py

Authentication Database Operations
"""

from database.database import db

import hashlib


# ---------------------------------------------------
# Password Hashing
# ---------------------------------------------------

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# ---------------------------------------------------
# Register User
# ---------------------------------------------------

def register_user(
    name,
    email,
    password
):

    existing = db.fetchone(

        "SELECT * FROM users WHERE email=?",

        (email,)

    )

    if existing:

        return False, "Email already exists."

    hashed = hash_password(password)

    db.execute(

        """
        INSERT INTO users(
            name,
            email,
            password
        )
        VALUES(?,?,?)
        """,

        (
            name,
            email,
            hashed
        )

    )

    return True, "Registration Successful."


# ---------------------------------------------------
# Login
# ---------------------------------------------------

def login_user(
    email,
    password
):

    hashed = hash_password(password)

    user = db.fetchone(

        """
        SELECT * FROM users

        WHERE email=?

        AND password=?
        """,

        (
            email,
            hashed
        )

    )

    if user:

        return dict(user)

    return None


# ---------------------------------------------------
# Get User
# ---------------------------------------------------

def get_user_by_email(email):

    user = db.fetchone(

        """

        SELECT *

        FROM users

        WHERE email=?

        """,

        (email,)

    )

    if user:

        return dict(user)

    return None


# ---------------------------------------------------
# Update Password
# ---------------------------------------------------

def update_password(
    email,
    new_password
):

    hashed = hash_password(
        new_password
    )

    db.execute(

        """

        UPDATE users

        SET password=?

        WHERE email=?

        """,

        (
            hashed,
            email
        )

    )

    return True


# ---------------------------------------------------
# Delete User
# ---------------------------------------------------

def delete_user(user_id):

    db.execute(

        """

        DELETE FROM users

        WHERE id=?

        """,

        (user_id,)

    )

    return True


# ---------------------------------------------------
# User Exists
# ---------------------------------------------------

def user_exists(email):

    user = db.fetchone(

        """

        SELECT id

        FROM users

        WHERE email=?

        """,

        (email,)

    )

    return user is not None


# ---------------------------------------------------
# Get User ID
# ---------------------------------------------------

def get_user_id(email):

    user = db.fetchone(

        """

        SELECT id

        FROM users

        WHERE email=?

        """,

        (email,)

    )

    if user:

        return user["id"]

    return None


# ---------------------------------------------------
# Save Resume Details
# ---------------------------------------------------

def save_resume(
    user_id,
    name,
    email,
    phone,
    skills,
    resume_path
):

    db.execute(

        """

        INSERT INTO resumes(

            user_id,

            name,

            email,

            phone,

            skills,

            resume_path

        )

        VALUES(?,?,?,?,?,?)

        """,

        (

            user_id,

            name,

            email,

            phone,

            ",".join(skills),

            resume_path

        )

    )


# ---------------------------------------------------
# Get Resume
# ---------------------------------------------------

def get_resume(user_id):

    resume = db.fetchone(

        """

        SELECT *

        FROM resumes

        WHERE user_id=?

        """,

        (user_id,)

    )

    if not resume:

        return None

    data = dict(resume)

    data["skills"] = data["skills"].split(",")

    return data