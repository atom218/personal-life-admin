import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from groq_client import extract_task


test_emails = [

    """
    Hi Vandan,

    Please submit the first draft of your independent study report
    by Friday at 5 PM. Make sure the experiment results are included.

    Thanks,
    Professor
    """,

    """
    Hi Vandan,

    Here are this week's machine learning engineering job openings.
    We found 15 positions that may be relevant to your background.

    Best,
    Job Alerts
    """,

    """
    Hi Vandan,

    Please review the attached project proposal and send me your
    feedback by Wednesday.

    Thanks,
    Professor
    """,

    """
    Your Amazon order has been delivered.

    Your package was left at your front door.
    """,

]


for i, email in enumerate(test_emails, start=1):

    print(f"\n{'=' * 70}")
    print(f"TEST EMAIL {i}")
    print("=" * 70)

    task = extract_task(email)

    print(task.model_dump_json(indent=2))