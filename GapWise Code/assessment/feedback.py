"""
assessment/feedback.py

Collects user feedback after assessment and updates
the adaptive learning module.
"""

import streamlit as st


class AssessmentFeedback:

    def __init__(self):

        if "assessment_feedback" not in st.session_state:
            st.session_state.assessment_feedback = {}

    # --------------------------------------------------
    # Feedback Form
    # --------------------------------------------------

    def collect_feedback(self):

        st.title("📝 Assessment Feedback")

        st.write(
            "Tell us about your experience with this assessment - "
            "what felt hard, what you're confident about, and any "
            "suggestions for what comes next."
        )

        comments = st.text_area(
            "Your feedback",
            height=180,
            placeholder=(
                "e.g. The Docker questions were tough, I felt more "
                "confident with Python. I'd like more beginner-level "
                "practice before retaking this."
            )
        )

        submitted = st.button(

            "Submit Feedback",

            use_container_width=True

        )

        if submitted:

            if not comments.strip():

                st.warning("Please share a few words of feedback before submitting.")

                return None

            feedback = {

                "comments": comments.strip()

            }

            st.session_state.assessment_feedback = feedback

            st.success(
                "Feedback Submitted Successfully."
            )

            return feedback

        return None


# --------------------------------------------------
# Recommendation
# --------------------------------------------------

def recommendation_from_feedback(
        feedback,
        score
):

    text = feedback.get("comments", "").lower()

    hard_signals = [
        "hard", "difficult", "struggled", "struggle", "confused",
        "tough", "couldn't", "cant", "can't", "unsure", "lost",
        "not confident", "overwhelmed"
    ]

    easy_signals = [
        "easy", "confident", "simple", "comfortable", "well",
        "good grasp", "ready", "strong", "clear"
    ]

    hard_count = sum(1 for w in hard_signals if w in text)

    easy_count = sum(1 for w in easy_signals if w in text)

    if hard_count > easy_count:

        return {

            "difficulty": "Beginner",

            "hours": 3,

            "recommendation":
                "Your feedback suggests some concepts felt difficult. "
                "We recommend revisiting fundamentals with beginner-level "
                "resources before retaking the assessment."

        }

    elif easy_count > hard_count:

        return {

            "difficulty": "Advanced",

            "hours": 1,

            "recommendation":
                "Your feedback suggests you're feeling confident. "
                "We recommend moving on to advanced material and "
                "real-world projects."

        }

    else:

        return {

            "difficulty": "Intermediate",

            "hours": 2,

            "recommendation":
                "Based on your feedback, we recommend continuing at a "
                "steady, intermediate pace with the current roadmap."

        }


# --------------------------------------------------
# Display Recommendation
# --------------------------------------------------

def display_feedback_result(
        recommendation
):

    st.divider()

    st.subheader("🎯 Personalized Recommendation")

    st.info(

        recommendation["recommendation"]

    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "Recommended Level",

            recommendation["difficulty"]

        )

    with col2:

        st.metric(

            "Suggested Study Hours / Day",

            recommendation["hours"]

        )


# --------------------------------------------------
# Complete Pipeline
# --------------------------------------------------

def run_feedback(
        assessment_score
):

    feedback_engine = AssessmentFeedback()

    feedback = feedback_engine.collect_feedback()

    if feedback:

        recommendation = recommendation_from_feedback(

            feedback,

            assessment_score

        )

        display_feedback_result(

            recommendation

        )

        return recommendation

    return None