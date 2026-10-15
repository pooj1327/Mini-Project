"""
reports/pdf_report.py

Generates a downloadable PDF Report
"""

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)


class PDFReport:

    def __init__(
        self,
        report,
        filename="GapWise_Report.pdf"
    ):

        self.report = report
        self.filename = filename

        self.styles = getSampleStyleSheet()

    # ------------------------------------------------

    def heading(self, text):

        return Paragraph(
            f"<b><font size=18>{text}</font></b>",
            self.styles["Title"]
        )

    # ------------------------------------------------

    def subheading(self, text):

        return Paragraph(
            f"<b><font size=13>{text}</font></b>",
            self.styles["Heading2"]
        )

    # ------------------------------------------------

    def paragraph(self, text):

        return Paragraph(
            str(text),
            self.styles["BodyText"]
        )

    # ------------------------------------------------

    def build(self):

        doc = SimpleDocTemplate(
            self.filename
        )

        story = []

        # ----------------------------------------

        story.append(
            self.heading("GapWise AI Report")
        )

        story.append(Spacer(1, 20))

        # ----------------------------------------

        story.append(
            self.subheading("Student Information")
        )

        story.append(
            self.paragraph(
                f"Name : {self.report['name']}"
            )
        )

        story.append(
            self.paragraph(
                f"Email : {self.report['email']}"
            )
        )

        story.append(
            self.paragraph(
                f"Generated On : {self.report['generated_on']}"
            )
        )

        story.append(Spacer(1, 15))

        # ----------------------------------------

        story.append(
            self.subheading("Job Information")
        )

        story.append(
            self.paragraph(
                f"Role : {self.report['job_role']}"
            )
        )

        story.append(
            self.paragraph(
                f"Deadline : {self.report['deadline']}"
            )
        )

        story.append(Spacer(1, 15))

        # ----------------------------------------

        story.append(
            self.subheading("Skill Gap Summary")
        )

        story.append(
            self.paragraph(
                f"Detected Skills : {self.report['skills_detected']}"
            )
        )

        story.append(
            self.paragraph(
                f"Matched Skills : {self.report['matched_skills']}"
            )
        )

        story.append(
            self.paragraph(
                f"Missing Skills : {self.report['missing_skills']}"
            )
        )

        story.append(
            self.paragraph(
                f"Skill Match : {self.report['skill_match']}%"
            )
        )

        story.append(
            self.paragraph(
                f"Readiness Score : {self.report['readiness']}%"
            )
        )

        story.append(Spacer(1, 15))

        # ----------------------------------------

        story.append(
            self.subheading("Assessment")
        )

        story.append(
            self.paragraph(
                f"Score : {self.report['assessment_score']}%"
            )
        )

        story.append(
            self.paragraph(
                f"Grade : {self.report['grade']}"
            )
        )

        story.append(
            self.paragraph(
                f"Performance : {self.report['performance']}"
            )
        )

        story.append(
            self.paragraph(
                self.report["recommendation"]
            )
        )

        story.append(Spacer(1, 15))

        # ----------------------------------------

        story.append(
            self.subheading("Matched Skills")
        )

        for skill in self.report["matched_skills"]:

            story.append(
                self.paragraph(
                    "• " + skill
                )
            )

        story.append(Spacer(1, 10))

        # ----------------------------------------

        story.append(
            self.subheading("Missing Skills")
        )

        for skill in self.report["missing_skills"]:

            story.append(
                self.paragraph(
                    "• " + skill
                )
            )

        story.append(Spacer(1, 10))

        # ----------------------------------------

        story.append(
            self.subheading("Learning Roadmap")
        )

        for task in self.report["learning_plan"]:

            story.append(

                self.paragraph(

                    f"{task['skill']} : "

                    f"{task['status']} "

                    f"({task['progress']}%)"

                )

            )

        story.append(Spacer(1, 15))

        # ----------------------------------------

        story.append(
            self.subheading("Roadmap Progress")
        )

        story.append(

            self.paragraph(

                f"Completed : "

                f"{self.report['roadmap']['completed']}"

            )

        )

        story.append(

            self.paragraph(

                f"Pending : "

                f"{self.report['roadmap']['pending']}"

            )

        )

        story.append(

            self.paragraph(

                f"Overall Progress : "

                f"{self.report['roadmap']['progress']}%"

            )

        )

        story.append(Spacer(1, 15))

        # ----------------------------------------

        story.append(
            self.subheading("User Feedback")
        )

        story.append(

            self.paragraph(

                str(self.report["feedback"])

            )

        )

        # ----------------------------------------

        doc.build(story)

        return self.filename


# --------------------------------------------------------

def create_pdf(report):

    pdf = PDFReport(report)

    return pdf.build()