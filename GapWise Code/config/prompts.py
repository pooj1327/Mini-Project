"""
config/prompts.py

LLM Prompts used throughout GapWise
"""


# -------------------------------------------------------
# Resume Parsing
# -------------------------------------------------------

RESUME_PARSER_PROMPT = """
You are an expert resume parser.

Extract only the following information.

1. Full Name

2. Email Address

3. Skills

Return ONLY valid JSON.

Example:

{
"name":"",
"email":"",
"skills":[]
}
"""


# -------------------------------------------------------
# Job Description Analysis
# -------------------------------------------------------

JOB_ANALYZER_PROMPT = """
You are an AI Job Analyzer.

Read the Job Description.

Extract

- Job Title

- Required Skills

- Preferred Skills

- Experience

Return JSON only.
"""


# -------------------------------------------------------
# Skill Gap
# -------------------------------------------------------

SKILL_GAP_PROMPT = """
Compare

Candidate Skills

and

Required Skills.

Return

Matched Skills

Missing Skills

Extra Skills

Skill Match Percentage

Readiness Score

Return JSON only.
"""


# -------------------------------------------------------
# Resource Recommendation
# -------------------------------------------------------

RESOURCE_PROMPT = """
Recommend

the best learning resources

for each missing skill.

Include

YouTube

Coursera

Udemy

freeCodeCamp

Official Documentation

GitHub

GeeksforGeeks

Roadmap.sh

Return JSON.
"""


# -------------------------------------------------------
# MCQ Generation
# -------------------------------------------------------

MCQ_PROMPT = """
Generate

5 MCQs

for the following skill.

Each question must contain

Question

4 Options

Correct Answer

Explanation

Return JSON.
"""


# -------------------------------------------------------
# Coding Questions
# -------------------------------------------------------

CODING_PROMPT = """
Generate

one coding interview question

for the skill.

Also provide

Difficulty

Expected Output

Constraints

Hidden Test Cases

Return JSON.
"""


# -------------------------------------------------------
# Code Evaluation
# -------------------------------------------------------

CODE_EVALUATION_PROMPT = """
Evaluate the submitted code.

Check

Correctness

Efficiency

Best Practices

Time Complexity

Space Complexity

Return

Score out of 100

Feedback

Improved Code

Explanation

Return JSON.
"""


# -------------------------------------------------------
# Adaptive Learning
# -------------------------------------------------------

ROADMAP_PROMPT = """
Generate

a personalized roadmap

based on

Missing Skills

Deadline

Assessment Score

Feedback

Study Hours

Return JSON.
"""


# -------------------------------------------------------
# Feedback Analysis
# -------------------------------------------------------

FEEDBACK_PROMPT = """
Analyze

the user's assessment feedback.

Recommend

Difficulty

Resources

Daily Hours

Revision Plan

Return JSON.
"""


# -------------------------------------------------------
# Report Summary
# -------------------------------------------------------

REPORT_PROMPT = """
Generate

a professional assessment summary.

Include

Strengths

Weaknesses

Recommendations

Learning Suggestions

Career Readiness

Return Markdown.
"""