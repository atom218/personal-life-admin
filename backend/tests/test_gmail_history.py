import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from gmail_client import get_profile, get_history


def test_gmail_history():
    profile = get_profile()

    print("\nGmail profile:")
    print(profile)

    history_id = profile.get("historyId")

    assert history_id is not None

    print(f"\nCurrent history ID: {history_id}")

    history = get_history(history_id)

    print("\nHistory response:")
    print(history)

    assert isinstance(history, dict)