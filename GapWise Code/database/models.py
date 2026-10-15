from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Text
from sqlalchemy import Boolean

from sqlalchemy.orm import declarative_base

from database.database import engine

Base = declarative_base()


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    email = Column(String, unique=True)

    password = Column(String)

    cgpa = Column(Float)

    college = Column(String)

    department = Column(String)

    semester = Column(Integer)


class Resume(Base):

    __tablename__ = "resume"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    skills = Column(Text)

    education = Column(Text)

    projects = Column(Text)

    certificates = Column(Text)


class Progress(Base):

    __tablename__ = "progress"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    completed = Column(Integer)

    total = Column(Integer)

    percentage = Column(Float)


class Assessment(Base):

    __tablename__ = "assessment"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    score = Column(Float)

    feedback = Column(Text)


Base.metadata.create_all(bind=engine)