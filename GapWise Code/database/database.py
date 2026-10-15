"""
database/database.py

SQLite Database Connection and Initialization
"""

import sqlite3
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_DIR = Path("data")
DATABASE_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "gapwise.db"

# ---------------------------------------------------
# SQLAlchemy Engine / Session
# (used by the SQLAlchemy-based models in database/models.py
# and by the authentication pages)
# ---------------------------------------------------

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}",
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(
            DATABASE_PATH,
            check_same_thread=False
        )

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        self.create_tables()

    # --------------------------------------------------

    def create_tables(self):

        # Users

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            email TEXT UNIQUE,

            password TEXT,

            cgpa REAL,

            college TEXT,

            department TEXT,

            semester INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)

        # Resume

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS resumes(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            name TEXT,

            email TEXT,

            phone TEXT,

            skills TEXT,

            resume_path TEXT,

            FOREIGN KEY(user_id)

            REFERENCES users(id)

        )

        """)

        # Job Description

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS jobs(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            job_description TEXT,

            required_skills TEXT,

            deadline TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)

            REFERENCES users(id)

        )

        """)

        # Roadmap

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS roadmap(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            skill TEXT,

            status TEXT,

            progress INTEGER,

            completed INTEGER,

            start_date TEXT,

            end_date TEXT,

            FOREIGN KEY(user_id)

            REFERENCES users(id)

        )

        """)

        # Assessments

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS assessments(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            mcq_score REAL,

            coding_score REAL,

            final_score REAL,

            grade TEXT,

            performance TEXT,

            assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)

            REFERENCES users(id)

        )

        """)

        # Feedback

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS feedback(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            difficulty TEXT,

            confidence INTEGER,

            satisfaction INTEGER,

            recommendation TEXT,

            comments TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)

            REFERENCES users(id)

        )

        """)

        # Progress Table

        self.cursor.execute("""

	CREATE TABLE IF NOT EXISTS progress(

    	id INTEGER PRIMARY KEY AUTOINCREMENT,

    	user_id INTEGER UNIQUE,

    	overall_progress REAL DEFAULT 0,

    	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

   	FOREIGN KEY(user_id)

    	REFERENCES users(id)

	)

	""")

        self.connection.commit()

    # --------------------------------------------------

    def execute(

        self,

        query,

        values=()

    ):

        self.cursor.execute(

            query,

            values

        )

        self.connection.commit()

    # --------------------------------------------------

    def fetchone(

        self,

        query,

        values=()

    ):

        self.cursor.execute(

            query,

            values

        )

        return self.cursor.fetchone()

    # --------------------------------------------------

    def fetchall(

        self,

        query,

        values=()

    ):

        self.cursor.execute(

            query,

            values

        )

        return self.cursor.fetchall()

    # --------------------------------------------------

    def close(self):

        self.connection.close()


db = Database()