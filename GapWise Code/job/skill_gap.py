"""
job/skill_gap.py

Final Skill Gap Analysis Module
Generates dashboard-ready results from Resume and Job Description.
"""

import streamlit as st

from job.matcher import SkillMatcher


class SkillGapAnalyzer:

    def __init__(
        self,
        resume_text,
        job_description,
        resume_skills,
        job_skills
    ):

        self.matcher = SkillMatcher(
            resume_text=resume_text,
            job_description=job_description,
            resume_skills=resume_skills,
            job_skills=job_skills
        )

    # --------------------------------------------------
    # Complete Analysis
    # --------------------------------------------------

    def analyze(self):

        report = self.matcher.summary()

        total_required = len(report["matched_skills"]) + len(report["missing_skills"])

        completed = len(report["matched_skills"])

        progress = (
            round((completed / total_required) * 100, 2)
            if total_required > 0
            else 0
        )

        dashboard = {

            "skill_match": report["skill_match"],

            "readiness_score": report["readiness_score"],

            "match_level": report["match_level"],

            "matched_skills": report["matched_skills"],

            "missing_skills": report["missing_skills"],

            "extra_skills": report["extra_skills"],

            "semantic_similarity": report["semantic_similarity"],

            "tfidf_similarity": report["tfidf_similarity"],

            "progress": progress,

            "completed_skills": completed,

            "remaining_skills": len(report["missing_skills"]),

            "total_required_skills": total_required
        }

        return dashboard


# --------------------------------------------------
# Dashboard UI
# --------------------------------------------------

def display_skill_gap(result):

    st.title("🎯 Skill Gap Analysis")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Skill Match",
        f"{result['skill_match']}%"
    )

    c2.metric(
        "Readiness",
        f"{result['readiness_score']}%"
    )

    c3.metric(
        "Progress",
        f"{result['progress']}%"
    )

    c4.metric(
        "Level",
        result["match_level"]
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("✅ Matched Skills")

        if result["matched_skills"]:

            for skill in result["matched_skills"]:

                st.success(skill)

        else:

            st.info("No matched skills.")

    with col2:

        st.subheader("❌ Missing Skills")

        if result["missing_skills"]:

            for skill in result["missing_skills"]:

                st.error(skill)

        else:

            st.success("No missing skills.")

    st.divider()

    st.subheader("⭐ Additional Skills")

    if result["extra_skills"]:

        for skill in result["extra_skills"]:

            st.info(skill)

    else:

        st.write("No additional skills.")

    st.divider()

    st.subheader("Overall Progress")

    st.progress(result["progress"] / 100)

    st.caption(
        f"{result['completed_skills']} / "
        f"{result['total_required_skills']} Skills Matched"
    )


# --------------------------------------------------
# Complete Pipeline
# --------------------------------------------------

def run_skill_gap_analysis(
    resume_text,
    job_description,
    resume_skills,
    job_skills
):

    analyzer = SkillGapAnalyzer(
        resume_text,
        job_description,
        resume_skills,
        job_skills
    )

    result = analyzer.analyze()

    return result