"""
view_feedback.py

Feedback is collected silently in the background - learners submit it
on the Assessment page and it goes straight into the `feedback` table.
There is deliberately no feedback tab in the app UI.

This script is how you read it.

    python view_feedback.py              # print to terminal
    python view_feedback.py --csv        # also write feedback_export.csv
"""

import sys

from database.assessment_db import get_all_feedback


def main():

    rows = get_all_feedback()

    if not rows:
        print("No feedback submitted yet.")
        return

    print(f"\n{len(rows)} feedback submission(s), newest first:\n")

    for row in rows:

        print("-" * 60)
        print(f"  user       : {row.get('user_name')} <{row.get('user_email')}>")
        print(f"  submitted  : {row.get('created_at')}")
        print(f"  difficulty : {row.get('difficulty')}")
        print(f"  suggested  : {row.get('recommendation')}")

        comments = (row.get("comments") or "").strip()

        if comments:
            print(f"  comments   : {comments}")

    print("-" * 60)

    if "--csv" in sys.argv:

        import csv

        out = "feedback_export.csv"

        with open(out, "w", newline="", encoding="utf-8") as handle:

            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))

            writer.writeheader()

            writer.writerows(rows)

        print(f"\nWritten to {out}")


if __name__ == "__main__":
    main()
