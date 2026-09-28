import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from email_processor import process_email


USER_ID = "test-user"


def test_process_email():
    message_id = "1a0e4a6ec05e4f36"

    result = process_email(
        user_id=USER_ID,
        message_id=message_id,
    )

    print(f"Result: {result}")

    assert result in {
        "already_processed",
        "empty",
        "filtered",
        "task_created",
        "no_task",
    }


if __name__ == "__main__":
    test_process_email()