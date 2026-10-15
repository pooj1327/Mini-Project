"""
roadmap/roadmap_generator.py

Generates a personalized learning roadmap based on:
- Missing Skills
- Selected Resources
- Deadline
"""

from datetime import datetime, timedelta


class RoadmapGenerator:

    def __init__(
        self,
        missing_skills,
        selected_resources,
        deadline
    ):

        self.missing_skills = missing_skills
        self.selected_resources = selected_resources
        self.deadline = deadline

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
    # Generate Roadmap
    # --------------------------------------------------

    def generate(self):

        total_days = self.days_remaining()

        total_skills = max(len(self.missing_skills), 1)

        base_days = max(1, total_days // total_skills)

        # Floor division silently discards the remainder (e.g. 10 days
        # over 3 skills used to give every skill 3 days, quietly
        # dropping the 10th day). Hand that remainder out one extra
        # day at a time to the earliest skills instead, so the roadmap
        # always accounts for the full deadline window.
        remainder = max(0, total_days - (base_days * total_skills))

        roadmap = []

        current = datetime.today().date()

        for index, skill in enumerate(self.missing_skills):

            days_for_skill = base_days + (1 if index < remainder else 0)

            start = current

            end = current + timedelta(days=days_for_skill - 1)

            roadmap.append({

                "skill": skill,

                "start_date": str(start),

                "end_date": str(end),

                "status": "Pending",

                "progress": 0,

                "completed": False,

                "resources": self.selected_resources.get(
                    skill,
                    []
                )

            })

            current = end + timedelta(days=1)

        return roadmap


# --------------------------------------------------
# Helper Function
# --------------------------------------------------

def get_completed_resources(roadmap):
    """
    Returns {skill: [resource, ...]} containing ONLY the resources the
    learner has actually ticked as completed on the Roadmap page.

    This is what the assessment is generated from - questions must
    come from material the learner has genuinely finished, not from
    everything they merely selected at the start.

    Skills with no completed resources are omitted entirely.
    """

    completed = {}

    for task in (roadmap or []):

        skill = task.get("skill")

        done_resources = [
            r for r in task.get("resources", [])
            if r.get("completed")
        ]

        if done_resources:
            completed[skill] = done_resources

    return completed


def generate_learning_roadmap(
        missing_skills,
        selected_resources,
        deadline
):

    generator = RoadmapGenerator(

        missing_skills,

        selected_resources,

        deadline

    )

    return generator.generate()