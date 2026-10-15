"""
reports/analytics.py

Analytics Dashboard for GapWise
"""

import pandas as pd
import plotly.express as px
import streamlit as st


class Analytics:

    def __init__(
        self,
        report
    ):

        self.report = report

    # ------------------------------------------------
    # Skill Distribution
    # ------------------------------------------------

    def skill_distribution(self):

        matched = len(
            self.report["matched_skills"]
        )

        missing = len(
            self.report["missing_skills"]
        )

        extra = len(
            self.report["extra_skills"]
        )

        df = pd.DataFrame({

            "Category": [

                "Matched",

                "Missing",

                "Extra"

            ],

            "Count": [

                matched,

                missing,

                extra

            ]

        })

        fig = px.pie(

            df,

            values="Count",

            names="Category",

            hole=0.5,

            title="Skill Distribution"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    # ------------------------------------------------
    # Assessment Analytics
    # ------------------------------------------------

    def assessment_chart(self):

        df = pd.DataFrame({

            "Metric": [

                "Skill Match",

                "Readiness",

                "Assessment"

            ],

            "Score": [

                self.report["skill_match"],

                self.report["readiness"],

                self.report["assessment_score"]

            ]

        })

        fig = px.bar(

            df,

            x="Metric",

            y="Score",

            text="Score",

            title="Performance"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    # ------------------------------------------------
    # Roadmap Analytics
    # ------------------------------------------------

    def roadmap_chart(self):

        roadmap = self.report["learning_plan"]

        df = pd.DataFrame({

            "Skill":

                [

                    x["skill"]

                    for x in roadmap

                ],

            "Progress":

                [

                    x["progress"]

                    for x in roadmap

                ]

        })

        fig = px.bar(

            df,

            x="Skill",

            y="Progress",

            text="Progress",

            title="Roadmap Progress"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    # ------------------------------------------------
    # MCQ vs Coding Score Breakdown (not shown elsewhere)
    # ------------------------------------------------

    def mcq_vs_coding_chart(self):

        df = pd.DataFrame({

            "Type": ["MCQ", "Coding"],

            "Score": [
                self.report.get("mcq_score", 0),
                self.report.get("coding_score", 0)
            ]

        })

        fig = px.bar(

            df,

            x="Type",

            y="Score",

            text="Score",

            title="MCQ vs Coding Performance",

            color="Type",

            color_discrete_sequence=["#7C3AED", "#22C55E"]

        )

        fig.update_layout(showlegend=False, yaxis_range=[0, 100])

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    # ------------------------------------------------
    # Resources Selected Per Skill (not shown elsewhere)
    # ------------------------------------------------

    def resources_per_skill_chart(self):

        learning_plan = self.report.get("learning_plan", [])

        if not learning_plan:
            st.info("No roadmap data available yet.")
            return

        df = pd.DataFrame({

            "Skill": [item["skill"] for item in learning_plan],

            "Resources Selected": [
                len(item.get("resources", [])) for item in learning_plan
            ]

        })

        fig = px.bar(

            df,

            x="Skill",

            y="Resources Selected",

            text="Resources Selected",

            title="Learning Resources Selected Per Skill",

            color_discrete_sequence=["#2563EB"]

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    # ------------------------------------------------
    # Skill Breakdown Table (data-dense view, distinct
    # from the Dashboard's donut chart)
    # ------------------------------------------------

    def skill_table(self):

        rows = []

        for skill in self.report["matched_skills"]:
            rows.append({"Skill": skill, "Status": "✅ Matched"})

        for skill in self.report["missing_skills"]:
            rows.append({"Skill": skill, "Status": "❌ Missing"})

        for skill in self.report["extra_skills"]:
            rows.append({"Skill": skill, "Status": "⭐ Extra"})

        if rows:

            df = pd.DataFrame(rows)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No skill data available yet.")

    # ------------------------------------------------
    # Display Analytics
    # ------------------------------------------------

    def display(self):

        st.title("📈 Analytics Dashboard")

        st.caption(
            "Deeper analysis not covered on the Dashboard: MCQ vs Coding "
            "performance, resource engagement, and the full skill "
            "breakdown table."
        )

        st.subheader("MCQ vs Coding Performance")

        self.mcq_vs_coding_chart()

        st.divider()

        st.subheader("Resource Engagement")

        self.resources_per_skill_chart()

        st.divider()

        st.subheader("Full Skill Breakdown")

        self.skill_table()


# ------------------------------------------------
# Helper Function
# ------------------------------------------------

def show_analytics(report):

    analytics = Analytics(report)

    analytics.display()