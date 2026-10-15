"""
resources/recommendation.py

Adaptive Recommendation Engine
Generates personalized recommendations based on
missing skills, selected resources, deadline,
assessment score and user feedback.
"""

from datetime import datetime


class RecommendationEngine:

    def __init__(
        self,
        missing_skills,
        selected_resources,
        deadline,
        assessment_score=0,
        feedback="Medium"
    ):

        self.missing_skills = missing_skills
        self.selected_resources = selected_resources
        self.deadline = deadline
        self.assessment_score = assessment_score
        self.feedback = feedback

    # --------------------------------------------------
    # Days Remaining
    # --------------------------------------------------

    def days_remaining(self):

        today = datetime.today().date()

        if isinstance(self.deadline, str):

            deadline = datetime.strptime(
                self.deadline,
                "%Y-%m-%d"
            ).date()

        else:

            deadline = self.deadline

        days = (deadline - today).days

        return max(days, 1)

    # --------------------------------------------------
    # Hours Per Day
    # --------------------------------------------------

    def study_hours(self):

        days = self.days_remaining()

        skills = max(len(self.missing_skills), 1)

        total_hours = skills * 8

        return round(total_hours / days, 1)

    # --------------------------------------------------
    # Difficulty
    # --------------------------------------------------

    def learning_level(self):

        feedback = self.feedback.lower()

        if feedback == "advanced" or feedback == "easy":
            return "Advanced"

        elif feedback == "beginner" or feedback == "hard":
            return "Beginner"

        return "Intermediate"

    # --------------------------------------------------
    # Feedback Recommendation
    # --------------------------------------------------

    def feedback_recommendation(self):

        feedback = self.feedback.lower()

        if feedback in ("advanced", "easy"):

            return (
                "Increase assessment difficulty and "
                "include advanced coding questions."
            )

        elif feedback in ("intermediate", "medium"):

            return (
                "Continue with the current roadmap."
            )

        return (
            "Recommend beginner tutorials, videos "
            "and additional practice questions."
        )

    # --------------------------------------------------
    # Skill Plan
    # --------------------------------------------------

    def skill_plan(self):

        plan = {}

        hours = self.study_hours()

        total_days = self.days_remaining()

        total_skills = max(len(self.missing_skills), 1)

        # Split the remaining days across each missing skill (same
        # logic as the roadmap generator) instead of giving every
        # skill the full, undivided days_remaining - that used to make
        # the estimate look identical ("1 day") no matter how many
        # skills or resources were actually selected.
        base_days = max(1, total_days // total_skills)

        remainder = max(0, total_days - (base_days * total_skills))

        for index, skill in enumerate(self.missing_skills):

            resources = self.selected_resources.get(
                skill,
                []
            )

            estimated_days = base_days + (1 if index < remainder else 0)

            plan[skill] = {

                "resources": resources,

                "hours_per_day": hours,

                "estimated_days": estimated_days,

                "status": "Pending"
            }

        return plan

    # --------------------------------------------------
    # Final Recommendation
    # --------------------------------------------------

    def generate(self):

        return {

            "days_remaining":
                self.days_remaining(),

            "study_hours_per_day":
                self.study_hours(),

            "learning_level":
                self.learning_level(),

            "recommendation":
                self.feedback_recommendation(),

            "learning_plan":
                self.skill_plan()
        }


# ------------------------------------------------------
# Helper Function
# ------------------------------------------------------

def generate_recommendation(
    missing_skills,
    selected_resources,
    deadline,
    assessment_score,
    feedback
):

    engine = RecommendationEngine(

        missing_skills=missing_skills,

        selected_resources=selected_resources,

        deadline=deadline,

        assessment_score=assessment_score,

        feedback=feedback

    )

    return engine.generate()