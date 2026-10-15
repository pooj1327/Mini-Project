"""
assessment/coding_engine.py

Coding Assessment Engine
Supports Python, SQL and other coding questions.
"""

import streamlit as st


class CodingAssessment:

    def __init__(self, questions):

        self.questions = questions

        if "coding_answers" not in st.session_state:
            st.session_state.coding_answers = {}

    # -------------------------------------------------
    # Display Coding Questions
    # -------------------------------------------------

    def display(self):

        st.title("💻 Coding Assessment")

        st.write(
            "Solve the following coding questions."
        )

        coding_questions = [
            q for q in self.questions
            if q["type"] == "coding"
        ]

        if len(coding_questions) == 0:

            st.info("No Coding Questions Available.")

            return

        for index, question in enumerate(coding_questions):

            st.subheader(f"Question {index+1}")

            st.write(question["question"])

            answer = st.text_area(

                "Write your solution",

                height=250,

                value=st.session_state.coding_answers.get(index, ""),

                key=f"coding_answer_{index}"

            )

            st.session_state.coding_answers[index] = answer

            st.divider()

    # -------------------------------------------------
    # Evaluate
    # -------------------------------------------------

    def evaluate(self):

        report = []

        score = 0

        coding_questions = [
            q for q in self.questions
            if q["type"] == "coding"
        ]

        total = len(coding_questions)

        for index, question in enumerate(coding_questions):

            answer = st.session_state.coding_answers.get(
                index,
                ""
            )

            if len(answer.strip()) > 20:

                obtained = 1

                status = "Submitted"

            else:

                obtained = 0

                status = "Incomplete"

            score += obtained

            report.append({

                "question": question["question"],

                "answer": answer,

                "status": status,

                "sample_solution": question.get("sample_solution", "")

            })

        percentage = round(

            (score / total) * 100,

            2

        ) if total else 0

        return {

            "score": score,

            "total": total,

            "percentage": percentage,

            "answers": report

        }

    # -------------------------------------------------
    # Results
    # -------------------------------------------------

    def show_results(self, report):

        st.header("Coding Assessment Report")

        st.metric(

            "Score",

            f"{report['score']} / {report['total']}"

        )

        st.metric(

            "Percentage",

            f"{report['percentage']} %"

        )

        st.progress(

            report["percentage"] / 100

        )

        st.divider()

        for item in report["answers"]:

            st.subheader(item["question"])

            st.code(

                item["answer"],

                language="python"

            )

            if item["status"] == "Submitted":

                st.success("Solution Submitted")

            else:

                st.error("Incomplete Solution")

            if item.get("sample_solution"):

                st.caption("Reference / sample solution:")

                st.code(

                    item["sample_solution"],

                    language="python"

                )

            st.divider()


# -------------------------------------------------
# Helper Function
# -------------------------------------------------

def run_coding_assessment(questions):

    engine = CodingAssessment(
        questions
    )

    engine.display()

    submit = st.button(

        "Submit Coding Assessment",

        use_container_width=True

    )

    if submit:

        report = engine.evaluate()

        st.session_state.coding_report = report

    if st.session_state.get("coding_report"):

        engine.show_results(st.session_state.coding_report)

    return st.session_state.get("coding_report")