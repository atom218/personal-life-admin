import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from groq_client import extract_task


TEST_EMAILS = [
    {
        "name": "OTP",
        "subject": "Your verification code",
        "sender": "security@example.com",
        "body": """
Your verification code is 482913.
Use this code to complete your login.
The code expires in 10 minutes.
""",
    },
    {
        "name": "Temporary access code",
        "subject": "Your Netflix temporary access code",
        "sender": "netflix@example.com",
        "body": """
Here is your temporary access code: 123456.
Enter this code to continue watching Netflix.
The code expires shortly.
""",
    },
    {
        "name": "Password confirmation",
        "subject": "Your password was changed",
        "sender": "security@example.com",
        "body": """
Your account password was successfully changed.
If you made this change, no further action is required.
""",
    },
    {
        "name": "Assignment deadline",
        "subject": "Assignment due Friday",
        "sender": "professor@university.edu",
        "body": """
Please submit your assignment by Friday at 5 PM.
""",
    },
    {
        "name": "Interview scheduling",
        "subject": "Schedule your interview",
        "sender": "recruiter@company.com",
        "body": """
We would like to schedule an interview with you.
Please select an available interview time using the scheduling link.
""",
    },
    {
        "name": "Professor feedback",
        "subject": "Please review my proposal",
        "sender": "professor@university.edu",
        "body": """
Please review the attached proposal and send me your feedback by Wednesday.
""",
    },
]


for email in TEST_EMAILS:
    print("=" * 70)
    print(f"TEST: {email['name']}")
    print("=" * 70)

    try:
        task = extract_task(
            subject=email["subject"],
            sender=email["sender"],
            body=email["body"],
        )

        print(task.model_dump_json(indent=2))

    except Exception as e:
        print(f"ERROR: {e}")

    print()