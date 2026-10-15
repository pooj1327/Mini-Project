"""
assessment/question_generator.py

Generates MCQ and Coding assessment questions for the skills a
candidate is missing, using Google Gemini.

This module wires up the MCQ_PROMPT / CODING_PROMPT templates that
already existed in config/prompts.py but were never connected to
anything, and produces the exact question format expected by
assessment/mcq_engine.py and assessment/coding_engine.py:

    mcq question  -> {"type": "mcq", "question", "options", "answer", "explanation"}
    coding question -> {"type": "coding", "question"}
"""

import json
import re

import streamlit as st
from google import genai

from config.config import GOOGLE_API_KEY, DEFAULT_MODEL, MCQ_PER_SKILL, CODING_PER_SKILL
from config.prompts import MCQ_PROMPT, CODING_PROMPT


# --------------------------------------------------
# Gemini Setup
# --------------------------------------------------

_client = None


def _get_client():

    global _client

    if not GOOGLE_API_KEY:
        return None

    if _client is None:
        _client = genai.Client(api_key=GOOGLE_API_KEY)

    return _client


def _extract_json(text):
    """
    Gemini sometimes wraps JSON in ```json fences or adds extra text.
    This pulls out the first {...} or [...] block and parses it.
    """

    text = text.strip()

    text = re.sub(r"^```json\s*|^```\s*|```$", "", text, flags=re.MULTILINE).strip()

    match = re.search(r"(\{.*\}|\[.*\])", text, flags=re.DOTALL)

    if not match:
        raise ValueError("No JSON found in model response.")

    data = json.loads(match.group(1))

    # Gemini sometimes wraps the array in an object
    # (e.g. {"questions": [...]}) despite being told to
    # return a bare array - unwrap it if so.
    if isinstance(data, dict):

        for value in data.values():

            if isinstance(value, list):
                return value

        raise ValueError("Expected a JSON array but got an object with no list inside.")

    return data

    return json.loads(match.group(1))


# --------------------------------------------------
# Fallback Questions (used if no API key / API failure)
# --------------------------------------------------

import random


# --------------------------------------------------
# Skills that don't lend themselves to a coding question
# (tools, platforms, and broad concepts rather than
# languages/libraries you write code in)
# --------------------------------------------------

NON_CODABLE_SKILLS = {
    "power bi", "tableau", "excel", "azure", "aws", "gcp",
    "docker", "kubernetes", "linux", "git", "github", "rest api",
    "machine learning", "deep learning", "nlp", "computer vision",
    "data analytics", "data science", "agentic ai", "generative ai",
    "llm"
}


def _is_codable(skill):
    return skill.strip().lower() not in NON_CODABLE_SKILLS


# --------------------------------------------------
# What each platform actually teaches, so the resource
# titles the user selected (e.g. "Python - GeeksforGeeks")
# can meaningfully scope the kind of question asked, not
# just be a decorative mention in the prompt.
# --------------------------------------------------

PLATFORM_CONTENT_FOCUS = {
    "Official Docs": "authoritative reference material covering the full breadth of the topic, including edge cases and formal definitions",
    "W3Schools": "beginner-friendly syntax, basic examples, and simple 'try it yourself' style usage",
    "freeCodeCamp": "beginner, hands-on tutorial content built around small practical exercises",
    "TutorialsPoint": "beginner/intermediate reference-style tutorials covering core syntax and standard usage patterns",
    "GeeksforGeeks": "fundamentals, common interview-style concepts, and standard implementation patterns",
    "YouTube": "practical, applied walkthroughs and demonstrations rather than formal theory",
    "Coursera": "structured, course-style conceptual material with a logical progression of topics",
    "edX": "structured, course-style conceptual material with a logical progression of topics",
    "Udemy": "project-oriented, intermediate-to-advanced practical application",
    "Medium": "intermediate/advanced articles focused on specific techniques, patterns, or real-world use cases",
    "GitHub": "real code examples, repositories, and advanced implementation details",
    "Kaggle": "applied, data-driven notebooks and hands-on practical problems",
    "Google": "a general web search, so treat it as broad practical/beginner-to-intermediate coverage",
}


def _resource_scope_text(resources):
    """
    Builds a strict, mandatory grounding block for the prompt from the
    resources the learner actually selected for this skill - not just
    their titles, but what that kind of resource typically teaches, so
    Gemini has a real basis to keep questions inside that scope.
    """

    if not resources:
        return ""

    lines = []

    for r in resources:

        title = r.get("title", "")
        platform = r.get("platform", "")
        focus = PLATFORM_CONTENT_FOCUS.get(platform, "practical, applied knowledge of the topic")

        lines.append(f'- "{title}" ({platform}): typically covers {focus}')

    resource_list = "\n".join(lines)

    return (
        "\nThe learner has committed to studying ONLY the following "
        "resources for this skill - not the full breadth of the "
        f"subject:\n{resource_list}\n\n"
        "STRICT REQUIREMENT: every question you generate MUST be "
        "answerable using knowledge that these specific resources "
        "would realistically teach. Do NOT introduce sub-topics, "
        "APIs, or concepts that go beyond what this combination of "
        "resources would cover. If the resources are beginner-focused, "
        "keep the questions beginner-level; if they are advanced or "
        "reference-style, you may go deeper - but always stay within "
        "the scope implied by the list above.\n"
    )


# --------------------------------------------------
# Fallback Questions (used if no API key / API failure)
# --------------------------------------------------

_MCQ_TEMPLATES = [
    lambda skill: {
        "question": f"Which statement best describes {skill}?",
        "options": [
            f"{skill} is a recognized skill/technology in this field",
            "It is a type of programming language error",
            "It is unrelated to software or data work",
            "It refers to a hardware component only"
        ],
        "answer": f"{skill} is a recognized skill/technology in this field",
        "explanation": (
            f"{skill} is a real, recognized skill in this field, distinct "
            "from unrelated technical or hardware terms."
        )
    },
    lambda skill: {
        "question": f"A candidate lists {skill} on their resume. What would you expect them to be able to do?",
        "options": [
            f"Apply {skill} to solve a relevant, practical task",
            "Nothing specific, it's just a buzzword",
            "Only explain the history of the term",
            "None of the above"
        ],
        "answer": f"Apply {skill} to solve a relevant, practical task",
        "explanation": (
            f"Listing {skill} implies practical, hands-on ability to "
            "apply it, not just familiarity with the term."
        )
    },
    lambda skill: {
        "question": f"Which of these is most closely associated with {skill}?",
        "options": [
            f"Core concepts and common use cases of {skill}",
            "An unrelated cooking technique",
            "A historical event with no technical link",
            "A random unrelated term"
        ],
        "answer": f"Core concepts and common use cases of {skill}",
        "explanation": (
            f"This question checks basic recognition of {skill}'s core "
            "concepts and typical use cases."
        )
    },
]

_CODING_TEMPLATES = [
    lambda skill: {
        "question": f"Write a short solution that demonstrates a practical, real-world use of {skill}.",
        "sample_solution": f"# A reference solution for {skill} would go here."
    },
    lambda skill: {
        "question": f"Describe and implement one common task you'd solve using {skill}.",
        "sample_solution": f"# A reference solution for {skill} would go here."
    },
    lambda skill: {
        "question": f"Given a simple real-world scenario, show how {skill} would be applied to address it.",
        "sample_solution": f"# A reference solution for {skill} would go here."
    },
]


def _fallback_mcq(skill, count):

    templates = _MCQ_TEMPLATES.copy()

    random.shuffle(templates)

    questions = []

    for i in range(count):

        template = templates[i % len(templates)]

        q = template(skill)

        q["type"] = "mcq"

        questions.append(q)

    return questions


def _fallback_coding(skill, count):

    templates = _CODING_TEMPLATES.copy()

    random.shuffle(templates)

    questions = []

    for i in range(count):

        template = templates[i % len(templates)]

        q = template(skill)

        q["type"] = "coding"

        questions.append(q)

    return questions


# --------------------------------------------------
# Gemini-backed Generation
# --------------------------------------------------

_last_error = None


def _generate_mcq_for_skill(skill, count, resources=None):

    global _last_error

    client = _get_client()

    if client is None:
        return _fallback_mcq(skill, count)

    seed = random.randint(1, 1_000_000)

    resource_context = _resource_scope_text(resources)

    prompt = (
        f"{MCQ_PROMPT}\n\nSkill: {skill}\n"
        f"{resource_context}"
        f"Generate exactly {count} DIFFERENT question(s) - no two questions "
        "should test the same exact concept or be reworded duplicates of "
        "each other. Vary the angle, scenario, or sub-topic for each one. "
        "Each question must have exactly one clearly correct answer among "
        "the options, and the options must be plausible (not filler like "
        "'none of the above' or 'a random term'). The 'answer' field must "
        "be copied EXACTLY, character-for-character, from one of the "
        "'options' - do not paraphrase it. "
        f"(variation seed: {seed})\n"
        "Return a JSON array, each item shaped like: "
        '{"question": "", "options": ["", "", "", ""], '
        '"answer": "", "explanation": ""}'
    )

    try:

        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt
        )

        data = _extract_json(response.text)

        questions = []

        for item in data[:count]:

            options = item["options"]

            answer = item["answer"]

            if answer not in options:

                # Model didn't copy the answer verbatim - try a
                # case-insensitive match before giving up on this item.
                match = next(
                    (o for o in options if o.strip().lower() == answer.strip().lower()),
                    None
                )

                if match is None:
                    continue

                answer = match

            questions.append({
                "type": "mcq",
                "question": item["question"],
                "options": options,
                "answer": answer,
                "explanation": item.get("explanation", "")
            })

        return questions if questions else _fallback_mcq(skill, count)

    except Exception as e:
        _last_error = f"MCQ generation for '{skill}' failed: {e}"
        return _fallback_mcq(skill, count)


def _generate_coding_for_skill(skill, count, resources=None):

    global _last_error

    client = _get_client()

    if client is None:
        return _fallback_coding(skill, count)

    seed = random.randint(1, 1_000_000)

    resource_context = _resource_scope_text(resources)

    prompt = (
        f"{CODING_PROMPT}\n\nSkill: {skill}\n"
        f"{resource_context}"
        f"Generate exactly {count} DIFFERENT question(s) - no two questions "
        "should test the same exact task. Vary the scenario or sub-topic "
        f"for each one. (variation seed: {seed})\n"
        "Return a JSON array, each item shaped like: "
        '{"question": "", "difficulty": "", "sample_solution": "", '
        '"expected_output": "", "constraints": ""}'
    )

    try:

        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt
        )

        data = _extract_json(response.text)

        questions = []

        for item in data[:count]:

            questions.append({
                "type": "coding",
                "question": item["question"],
                "sample_solution": item.get("sample_solution", "")
            })

        return questions if questions else _fallback_coding(skill, count)

    except Exception as e:
        _last_error = f"Coding question generation for '{skill}' failed: {e}"
        return _fallback_coding(skill, count)


# --------------------------------------------------
# Public Entry Point
# --------------------------------------------------

def generate_questions(skill_gap, selected_resources=None):
    """
    Builds the full assessment question set for every missing skill
    that the learner has actually selected resources for.

    Parameters
    ----------
    skill_gap : dict
        Result of job.skill_gap.run_skill_gap_analysis(...), must
        contain a "missing_skills" list.
    selected_resources : dict, optional
        {skill: [resource, ...]}. A skill with no resources selected
        is skipped entirely - questions are only generated for the
        resources the learner has actually committed to studying, and
        are grounded strictly in what those specific resources teach.

    Returns
    -------
    dict: {"mcq": [...], "coding": [...], "skipped_skills": [...], ...}
    """

    missing_skills = skill_gap.get("missing_skills", []) if skill_gap else []

    if not missing_skills:
        return {"mcq": [], "coding": [], "skipped_skills": []}

    mcq_questions = []
    coding_questions = []
    skipped_skills = []

    global _last_error
    _last_error = None

    no_key_configured = GOOGLE_API_KEY == ""

    with st.spinner("Generating questions with Gemini..."):

        for skill in missing_skills:

            resources = (selected_resources or {}).get(skill, [])

            if not resources:
                # No resources selected for this skill - there is
                # nothing to ground the questions in, so skip it
                # rather than asking broad, unscoped questions.
                skipped_skills.append(skill)
                continue

            for q in _generate_mcq_for_skill(skill, MCQ_PER_SKILL, resources):
                if q["question"] not in {x["question"] for x in mcq_questions}:
                    mcq_questions.append(q)

            if _is_codable(skill):

                for q in _generate_coding_for_skill(skill, CODING_PER_SKILL, resources):
                    if q["question"] not in {x["question"] for x in coding_questions}:
                        coding_questions.append(q)

    return {
        "mcq": mcq_questions,
        "coding": coding_questions,
        "skipped_skills": skipped_skills,
        "used_fallback": no_key_configured or _last_error is not None,
        "no_key_configured": no_key_configured,
        "error": _last_error
    }
