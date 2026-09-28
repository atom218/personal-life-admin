import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from gmail_sync import sync_gmail


USER_ID = "test-user"


def test_gmail_sync():

    result = sync_gmail(
        user_id=USER_ID,
    )

    print("\n")
    print("=" * 60)
    print("SYNC RESULT")
    print("=" * 60)
    print(result)

    assert "email" in result
    assert "messages_found" in result
    assert "tasks_created" in result