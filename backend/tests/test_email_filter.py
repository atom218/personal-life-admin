import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from email_filter import should_skip_email


test_cases = [
    (
        "Weekly Machine Learning Job Alerts",
        "Here are this week's recommended machine learning jobs.",
    ),
    (
        "Your Amazon order has been delivered",
        "Your package was delivered and left at your front door.",
    ),
    (
        "Please submit your independent study report",
        "Please submit your first draft by Friday at 5 PM.",
    ),
    (
        "Professor asks for feedback",
        "Please review the proposal and send me your feedback by Wednesday.",
    ),
    (
        "Registration deadline approaching",
        "Registration opens today. Please register before Friday.",
    ),
]


for i, (subject, body) in enumerate(test_cases, start=1):
    result = should_skip_email(subject, body)

    print("=" * 60)
    print(f"TEST {i}")
    print(f"Subject: {subject}")
    print(f"Skip: {result}")