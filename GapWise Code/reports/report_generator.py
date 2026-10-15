"""
reports/report_generator.py

Generates the complete GapWise Report
"""

from datetime import datetime


class ReportGenerator:

    def __init__(
        self,
        user,
        resume_data,
        job_data,
        skill_gap,
        roadmap,
        assessment,
        feedback
    ):

        self.user = user
        self.resume = resume_data
        self.job = job_data
        self.skill_gap = skill_gap
        self.roadmap = roadmap
        self.assessment = assessment
        self.feedback = feedback

    # --------------------------------------------------

    def summary(self):

        return {

            "generated_on": datetime.now().strftime(
                "%d-%m-%Y %H:%M"
            ),

            "name": self.resume["name"],

            "email": self.resume["email"],

            "job_role":
                self.job.get(
                    "job_title",
                    "Not Specified"
                ),

            "deadline":
                self.job["deadline"],

            "skills_detected":
                len(self.resume["skills"]),

            "matched_skills":
                len(self.skill_gap["matched_skills"]),

            "missing_skills":
                len(self.skill_gap["missing_skills"]),

            "skill_match":
                self.skill_gap["skill_match"],

            "readiness":
                self.skill_gap["readiness_score"],

            "assessment_score":
                self.assessment["final_score"],

            "mcq_score":
                self.assessment.get("mcq_score", 0),

            "coding_score":
                self.assessment.get("coding_score", 0),

            "grade":
                self.assessment["grade"],

            "performance":
                self.assessment["performance"],

            "recommendation":
                self.assessment["recommendation"],

            "feedback":
                self.feedback
        }

    # --------------------------------------------------

    def roadmap_summary(self):

        completed = 0

        pending = 0

        for skill in self.roadmap:

            if skill["completed"]:

                completed += 1

            else:

                pending += 1

        return {

            "completed": completed,

            "pending": pending,

            "progress":

                round(

                    completed

                    /

                    len(self.roadmap)

                    *

                    100,

                    2

                )

                if len(self.roadmap)

                else 0

        }

    # --------------------------------------------------

    def generate(self):

        report = self.summary()

        report["roadmap"] = self.roadmap_summary()

        report["matched_skills"] = \
            self.skill_gap["matched_skills"]

        report["missing_skills"] = \
            self.skill_gap["missing_skills"]

        report["extra_skills"] = \
            self.skill_gap["extra_skills"]

        report["learning_plan"] = self.roadmap

        return report


# ------------------------------------------------------

def generate_report(

    user,

    resume,

    job,

    skill_gap,

    roadmap,

    assessment,

    feedback

):

    generator = ReportGenerator(

        user,

        resume,

        job,

        skill_gap,

        roadmap,

        assessment,

        feedback

    )

    return generator.generate()