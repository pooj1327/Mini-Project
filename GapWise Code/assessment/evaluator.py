"""
assessment/evaluator.py

Combines MCQ and Coding Assessment Reports
Generates Final Assessment Score
"""

import streamlit as st


class AssessmentEvaluator:

    def __init__(self, mcq_report=None, coding_report=None):

        self.mcq_report = mcq_report
        self.coding_report = coding_report

    # --------------------------------------------------
    # MCQ Score
    # --------------------------------------------------

    def mcq_percentage(self):

        if self.mcq_report is None:
            return 0

        return self.mcq_report.get(
            "percentage",
            0
        )

    # --------------------------------------------------
    # Coding Score
    # --------------------------------------------------

    def coding_percentage(self):

        if self.coding_report is None:
            return 0

        return self.coding_report.get(
            "percentage",
            0
        )

    # --------------------------------------------------
    # Final Percentage
    # --------------------------------------------------

    def final_percentage(self):

        mcq = self.mcq_percentage()

        coding = self.coding_percentage()

        if self.mcq_report and self.coding_report:

            return round(
                (mcq + coding) / 2,
                2
            )

        elif self.mcq_report:

            return mcq

        elif self.coding_report:

            return coding

        return 0

    # --------------------------------------------------
    # Grade
    # --------------------------------------------------

    def grade(self):

        score = self.final_percentage()

        if score >= 90:
            return "A+"

        elif score >= 80:
            return "A"

        elif score >= 70:
            return "B"

        elif score >= 60:
            return "C"

        elif score >= 50:
            return "D"

        return "F"

    # --------------------------------------------------
    # Performance
    # --------------------------------------------------

    def performance(self):

        score = self.final_percentage()

        if score >= 90:
            return "Outstanding"

        elif score >= 80:
            return "Excellent"

        elif score >= 70:
            return "Very Good"

        elif score >= 60:
            return "Good"

        elif score >= 50:
            return "Average"

        return "Needs Improvement"

    # --------------------------------------------------
    # Recommendation
    # --------------------------------------------------

    def recommendation(self):

        score = self.final_percentage()

        if score >= 85:

            return (
                "Proceed to advanced topics and "
                "attempt harder assessments."
            )

        elif score >= 70:

            return (
                "Continue the roadmap and "
                "practice coding regularly."
            )

        elif score >= 50:

            return (
                "Revise concepts and complete "
                "additional learning resources."
            )

        return (
            "Restart the learning plan and "
            "practice fundamentals before retaking the assessment."
        )

    # --------------------------------------------------
    # Final Report
    # --------------------------------------------------

    def generate_report(self):

        return {

            "mcq_score":
                self.mcq_percentage(),

            "coding_score":
                self.coding_percentage(),

            "final_score":
                self.final_percentage(),

            "grade":
                self.grade(),

            "performance":
                self.performance(),

            "recommendation":
                self.recommendation()

        }


# --------------------------------------------------
# Display Report
# --------------------------------------------------

def display_final_report(report):

    st.title("🏆 Final Assessment Report")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Final Score",
        f"{report['final_score']}%"
    )

    col2.metric(
        "Grade",
        report["grade"]
    )

    col3.metric(
        "Performance",
        report["performance"]
    )

    st.progress(
        report["final_score"] / 100
    )

    st.success(
        report["recommendation"]
    )


# --------------------------------------------------
# Helper Function
# --------------------------------------------------

def evaluate_assessment(
    mcq_report=None,
    coding_report=None
):

    evaluator = AssessmentEvaluator(
        mcq_report,
        coding_report
    )

    report = evaluator.generate_report()

    display_final_report(report)

    return report