import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from gmail_sync_state import get_sync_state, save_sync_state


USER_ID = "test-user"
EMAIL_ADDRESS = "vandan28agrawal@gmail.com"


def test_gmail_sync_state():
    history_id = "4736807"

    save_sync_state(
        user_id=USER_ID,
        email_address=EMAIL_ADDRESS,
        history_id=history_id,
    )

    state = get_sync_state(
        user_id=USER_ID,
        email_address=EMAIL_ADDRESS,
    )

    print("\nGmail sync state:")
    print(state)

    assert state is not None
    assert state["email"] == EMAIL_ADDRESS
    assert state["history_id"] == history_id
    assert "last_synced_at" in state