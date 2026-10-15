"""
job/matcher.py

Matches resume skills with job description skills and
generates the matching report.
"""

from job.similarity import (
    analyze_similarity
)


class SkillMatcher:

    def __init__(
        self,
        resume_text,
        job_description,
        resume_skills,
        job_skills
    ):

        self.resume_text = resume_text
        self.job_description = job_description
        self.resume_skills = resume_skills
        self.job_skills = job_skills

    # ------------------------------------------
    # Run Skill Matching
    # ------------------------------------------

    def match(self):

        result = analyze_similarity(

            resume_text=self.resume_text,

            jd_text=self.job_description,

            resume_skills=self.resume_skills,

            jd_skills=self.job_skills

        )

        return result

    # ------------------------------------------
    # Match Level
    # ------------------------------------------

    @staticmethod
    def match_level(score):

        if score >= 90:
            return "Excellent"

        elif score >= 75:
            return "Very Good"

        elif score >= 60:
            return "Good"

        elif score >= 40:
            return "Average"

        return "Poor"

    # ------------------------------------------
    # Summary
    # ------------------------------------------

    def summary(self):

        report = self.match()

        return {

            "skill_match": report["match_percentage"],

            "readiness_score": report["readiness_score"],

            "semantic_similarity": report["semantic_similarity"],

            "tfidf_similarity": report["tfidf_similarity"],

            "matched_skills": report["matched_skills"],

            "missing_skills": report["missing_skills"],

            "extra_skills": report["extra_skills"],

            "match_level": self.match_level(
                report["match_percentage"]
            )
        }

    # ------------------------------------------
    # Print Report
    # ------------------------------------------

    def display_report(self):

        report = self.summary()

        print("\n========== Skill Gap Report ==========\n")

        print(
            f"Skill Match : {report['skill_match']} %"
        )

        print(
            f"Readiness Score : {report['readiness_score']}"
        )

        print(
            f"Semantic Similarity : {report['semantic_similarity']}"
        )

        print(
            f"TF-IDF Similarity : {report['tfidf_similarity']}"
        )

        print(
            f"Match Level : {report['match_level']}"
        )

        print("\nMatched Skills")

        print(report["matched_skills"])

        print("\nMissing Skills")

        print(report["missing_skills"])

        print("\nAdditional Skills")

        print(report["extra_skills"])

        print("\n=====================================")