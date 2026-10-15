"""
resources/resource_engine.py

Dynamic Resource Engine
Provides learning resources for any detected skill.
"""

from urllib.parse import quote_plus
import random


# -----------------------------------------------------------------
# Trusted Learning Platforms
# -----------------------------------------------------------------

LEARNING_PLATFORMS = {

    "YouTube":
        "https://www.youtube.com/results?search_query={}",

    "freeCodeCamp":
        "https://www.freecodecamp.org/news/search/?query={}",

    "Coursera":
        "https://www.coursera.org/search?query={}",

    "edX":
        "https://www.edx.org/search?q={}",

    "Udemy":
        "https://www.udemy.com/courses/search/?q={}",

    "GeeksforGeeks":
        "https://www.geeksforgeeks.org/?s={}",

    "W3Schools":
        "https://www.w3schools.com/search/search.asp?query={}",

    "TutorialsPoint":
        "https://www.tutorialspoint.com/index.htm?search={}",

    "Kaggle":
        "https://www.kaggle.com/search?q={}",

    "GitHub":
        "https://github.com/search?q={}",

    "Medium":
        "https://medium.com/search?q={}",

    "Google":
        "https://www.google.com/search?q={}"
}


# Which learner level each platform best serves. Used to re-rank
# resources when we know the learner's feedback-derived level.
PLATFORM_LEVELS = {
    "Official Docs": ["Beginner", "Intermediate", "Advanced"],
    "W3Schools": ["Beginner"],
    "freeCodeCamp": ["Beginner"],
    "TutorialsPoint": ["Beginner"],
    "GeeksforGeeks": ["Beginner", "Intermediate"],
    "YouTube": ["Beginner", "Intermediate"],
    "Coursera": ["Intermediate"],
    "edX": ["Intermediate"],
    "Udemy": ["Intermediate", "Advanced"],
    "Medium": ["Intermediate", "Advanced"],
    "GitHub": ["Advanced"],
    "Kaggle": ["Advanced"],
    "Google": ["Beginner", "Intermediate", "Advanced"],
}


# -----------------------------------------------------------------
# Official Documentation
# -----------------------------------------------------------------

OFFICIAL_DOCS = {

    "Python": "https://docs.python.org/3/",
    "Java": "https://docs.oracle.com/en/java/",
    "C++": "https://en.cppreference.com/",
    "SQL": "https://www.w3schools.com/sql/",
    "HTML": "https://developer.mozilla.org/en-US/docs/Web/HTML",
    "CSS": "https://developer.mozilla.org/en-US/docs/Web/CSS",
    "JavaScript": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
    "React": "https://react.dev/",
    "Angular": "https://angular.io/",
    "Vue": "https://vuejs.org/",
    "NodeJS": "https://nodejs.org/docs/latest/api/",
    "Django": "https://docs.djangoproject.com/",
    "Flask": "https://flask.palletsprojects.com/",
    "FastAPI": "https://fastapi.tiangolo.com/",
    "Pandas": "https://pandas.pydata.org/docs/",
    "NumPy": "https://numpy.org/doc/",
    "Matplotlib": "https://matplotlib.org/stable/",
    "Seaborn": "https://seaborn.pydata.org/",
    "Plotly": "https://plotly.com/python/",
    "TensorFlow": "https://www.tensorflow.org/",
    "PyTorch": "https://pytorch.org/docs/stable/index.html",
    "Scikit-Learn": "https://scikit-learn.org/stable/",
    "Docker": "https://docs.docker.com/",
    "Kubernetes": "https://kubernetes.io/docs/",
    "AWS": "https://docs.aws.amazon.com/",
    "Azure": "https://learn.microsoft.com/azure/",
    "GCP": "https://cloud.google.com/docs",
    "Git": "https://git-scm.com/doc",
    "GitHub": "https://docs.github.com/",
    "Power BI": "https://learn.microsoft.com/power-bi/",
    "Tableau": "https://help.tableau.com/",
    "Machine Learning": "https://developers.google.com/machine-learning",
    "Deep Learning": "https://www.deeplearningbook.org/",
    "NLP": "https://huggingface.co/docs",
    "LangChain": "https://python.langchain.com/docs/"
}


# -----------------------------------------------------------------
# Generate Dynamic Resources
# -----------------------------------------------------------------

_OFFICIAL_DOCS_LOWER = {k.lower(): v for k, v in OFFICIAL_DOCS.items()}


def _official_doc_url(skill):
    return _OFFICIAL_DOCS_LOWER.get(skill.strip().lower())


def get_resources(skill, level=None):
    """
    Returns resources for any skill, with the single best resource
    first (official docs when available), followed by a stable but
    skill-specific ordering of the remaining platforms so different
    skills don't all show the identical list in the identical order.

    If `level` ("Beginner"/"Intermediate"/"Advanced") is given, the
    platforms best suited to that level are promoted to the front
    of the remaining list.
    """

    encoded = quote_plus(skill)

    resources = []

    official_url = _official_doc_url(skill)

    if official_url:

        resources.append({

            "title": f"{skill} Official Documentation",

            "platform": "Official Docs",

            "url": official_url
        })

    # Deterministic per-skill shuffle: same skill always gets the same
    # order (so re-visiting the page doesn't reshuffle things), but
    # different skills get genuinely different orderings/subsets.
    platforms = list(LEARNING_PLATFORMS.items())

    rng = random.Random(skill.strip().lower())

    rng.shuffle(platforms)

    if level:

        platforms = [
            p for p in platforms if level in PLATFORM_LEVELS.get(p[0], [])
        ] or platforms  # never end up with an empty list

    # Cap to a reasonable number so the list doesn't feel like a
    # mechanical dump of every platform for every skill.
    platforms = platforms[:5]

    for platform, url in platforms:

        resources.append({

            "title": f"{skill} - {platform}",

            "platform": platform,

            "url": url.format(encoded)
        })

    return resources


# -----------------------------------------------------------------
# Generate Resources for Multiple Skills
# -----------------------------------------------------------------

def generate_resource_plan(missing_skills, level=None):
    """
    Returns a dictionary of resources for all missing skills.
    """

    plan = {}

    for skill in missing_skills:

        plan[skill] = get_resources(skill, level=level)

    return plan