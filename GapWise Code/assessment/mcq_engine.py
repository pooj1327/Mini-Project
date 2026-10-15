"""
assessment/mcq_engine.py

Dynamic MCQ Assessment Engine
"""

import streamlit as st


class MCQAssessment:

    def __init__(self, questions):

        self.questions = questions

        if "mcq_answers" not in st.session_state:
            st.session_state.mcq_answers = {}

    # --------------------------------------------------
    # Display Questions
    # --------------------------------------------------

    def display(self):

        st.title("📝 MCQ Assessment")

        st.write(
            "Answer all the questions and click Submit."
        )

        for i, question in enumerate(self.questions):

            if question["type"] != "mcq":
                continue

            st.subheader(f"Question {i+1}")

            st.write(question["question"])

            previous_answer = st.session_state.mcq_answers.get(i)

            default_index = (
                question["options"].index(previous_answer)
                if previous_answer in question["options"]
                else 0
            )

            answer = st.radio(

                "Choose an answer",

                question["options"],

                index=default_index,

                key=f"mcq_{i}"

            )

            st.session_state.mcq_answers[i] = answer

            st.divider()

    # --------------------------------------------------
    # Evaluate
    # --------------------------------------------------

    def evaluate(self):

        score = 0

        total = 0

        results = []

        for i, question in enumerate(self.questions):

            if question["type"] != "mcq":
                continue

            total += 1

            user_answer = st.session_state.mcq_answers.get(i)

            correct = question["answer"]

            is_correct = user_answer == correct

            if is_correct:
                score += 1

            results.append({

                "question": question["question"],

                "user_answer": user_answer,

                "correct_answer": correct,

                "correct": is_correct,

                "explanation": question["explanation"]

            })

        percentage = round(

            (score / total) * 100,

            2

        ) if total else 0

        return {

            "score": score,

            "total": total,

            "percentage": percentage,

            "results": results

        }

    # --------------------------------------------------
    # Results
    # --------------------------------------------------

    def show_results(self, report):

        st.header("Assessment Result")

        st.metric(

            "Score",

            f"{report['score']} / {report['total']}"

        )

        st.metric(

            "Percentage",

            f"{report['percentage']} %"

        )

        st.progress(report["percentage"] / 100)

        st.divider()

        for result in report["results"]:

            st.subheader(result["question"])

            st.write(

                "Your Answer :",

                result["user_answer"]

            )

            st.write(

                "Correct Answer :",

                result["correct_answer"]

            )

            if result["correct"]:

                st.success("Correct")

            else:

                st.error("Incorrect")

            st.info(

                result["explanation"]

            )

            st.divider()


# --------------------------------------------------
# Helper Function
# --------------------------------------------------

def run_mcq_assessment(questions):

    engine = MCQAssessment(questions)

    engine.display()

    submitted = st.button(

        "Submit Assessment",

        use_container_width=True

    )

    if submitted:

        report = engine.evaluate()

        st.session_state.mcq_report = report

    if st.session_state.get("mcq_report"):

        engine.show_results(st.session_state.mcq_report)

    return st.session_state.get("mcq_report")