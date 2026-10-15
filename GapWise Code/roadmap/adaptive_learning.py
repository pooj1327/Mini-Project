"""
roadmap/adaptive_learning.py

Adaptive Learning Engine

Updates the learning roadmap based on:
- Assessment Score
- User Feedback
- Progress
"""

from datetime import datetime, timedelta


class AdaptiveLearning:

    def __init__(
        self,
        roadmap,
        assessment_score,
        feedback
    ):

        self.roadmap = roadmap
        self.assessment_score = assessment_score
        self.feedback = feedback.lower()

    # -------------------------------------------------
    # Difficulty
    # -------------------------------------------------

    def difficulty(self):

        if self.assessment_score >= 85:
            return "Advanced"

        elif self.assessment_score >= 70:
            return "Intermediate"

        return "Beginner"

    # -------------------------------------------------
    # Extra Practice Required
    # -------------------------------------------------

    def extra_practice(self):

        return self.assessment_score < 70

    # -------------------------------------------------
    # Recommended Hours
    # -------------------------------------------------

    def recommended_hours(self):

        if self.assessment_score >= 85:
            return 1

        elif self.assessment_score >= 70:
            return 2

        return 3

    # -------------------------------------------------
    # Feedback Suggestions
    # -------------------------------------------------

    def recommendation(self):

        if self.feedback == "easy":

            return (
                "Increase difficulty. "
                "Add advanced coding questions."
            )

        elif self.feedback == "medium":

            return (
                "Continue with current roadmap."
            )

        elif self.feedback == "hard":

            return (
                "Provide beginner resources and "
                "additional practice."
            )

        return (
            "Continue learning."
        )

    # -------------------------------------------------
    # Adapt Roadmap
    # -------------------------------------------------

    def update(self):

        updated = []

        hours = self.recommended_hours()

        for task in self.roadmap:

            item = task.copy()

            item["difficulty"] = self.difficulty()

            item["recommended_hours"] = hours

            item["extra_practice"] = self.extra_practice()

            if (
                item["status"] != "Completed"
                and self.extra_practice()
            ):

                end = datetime.strptime(
                    item["end_date"],
                    "%Y-%m-%d"
                ).date()

                end += timedelta(days=1)

                item["end_date"] = str(end)

            updated.append(item)

        return updated


# -------------------------------------------------
# Helper Function
# -------------------------------------------------

def update_learning_plan(
    roadmap,
    assessment_score,
    feedback
):

    adaptive = AdaptiveLearning(

        roadmap=roadmap,

        assessment_score=assessment_score,

        feedback=feedback

    )

    return {

        "roadmap": adaptive.update(),

        "difficulty": adaptive.difficulty(),

        "recommended_hours": adaptive.recommended_hours(),

        "recommendation": adaptive.recommendation(),

        "extra_practice": adaptive.extra_practice()

    }