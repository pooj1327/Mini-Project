"""
job/similarity.py

Similarity functions used for Skill Gap Analysis.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sentence_transformers import SentenceTransformer


# ---------------------------------------------------
# Load Sentence Transformer Model
# ---------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# ---------------------------------------------------
# Cosine Similarity (TF-IDF)
# ---------------------------------------------------

def tfidf_similarity(text1: str, text2: str):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([text1, text2])

    similarity = cosine_similarity(
        vectors[0],
        vectors[1]
    )[0][0]

    return round(float(similarity), 3)


# ---------------------------------------------------
# Sentence Embedding Similarity
# ---------------------------------------------------

def semantic_similarity(text1: str, text2: str):

    embeddings = model.encode([text1, text2])

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(float(similarity), 3)


# ---------------------------------------------------
# Exact Skill Match
# ---------------------------------------------------

def skill_overlap(resume_skills, job_skills):

    resume = {skill.lower() for skill in resume_skills}

    job = {skill.lower() for skill in job_skills}

    matched = resume.intersection(job)

    missing = job.difference(resume)

    extra = resume.difference(job)

    return {

        "matched": sorted(list(matched)),

        "missing": sorted(list(missing)),

        "extra": sorted(list(extra))
    }


# ---------------------------------------------------
# Percentage Match
# ---------------------------------------------------

def match_percentage(resume_skills, job_skills):

    if len(job_skills) == 0:
        return 0

    overlap = skill_overlap(
        resume_skills,
        job_skills
    )

    percentage = (
        len(overlap["matched"])
        / len(job_skills)
    ) * 100

    return round(percentage, 2)


# ---------------------------------------------------
# Readiness Score
# ---------------------------------------------------

def readiness_score(
        match_percent,
        semantic_score
):

    score = (
        match_percent * 0.7
        +
        semantic_score * 100 * 0.3
    )

    return round(score, 2)


# ---------------------------------------------------
# Overall Analysis
# ---------------------------------------------------

def analyze_similarity(
        resume_text,
        jd_text,
        resume_skills,
        jd_skills
):

    semantic = semantic_similarity(
        resume_text,
        jd_text
    )

    tfidf = tfidf_similarity(
        resume_text,
        jd_text
    )

    overlap = skill_overlap(
        resume_skills,
        jd_skills
    )

    percentage = match_percentage(
        resume_skills,
        jd_skills
    )

    readiness = readiness_score(
        percentage,
        semantic
    )

    return {

        "semantic_similarity": semantic,

        "tfidf_similarity": tfidf,

        "match_percentage": percentage,

        "readiness_score": readiness,

        "matched_skills": overlap["matched"],

        "missing_skills": overlap["missing"],

        "extra_skills": overlap["extra"]
    }