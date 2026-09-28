from datetime import datetime, timezone

from firebase import db


def get_sync_state(user_id: str, email_address: str):
    """
    Get the stored Gmail sync state for an account.

    Returns None if this Gmail account has never been synced.
    """

    doc_ref = (
        db.collection("users")
        .document(user_id)
        .collection("gmail_accounts")
        .document(email_address)
    )

    document = doc_ref.get()

    if not document.exists:
        return None

    return document.to_dict()


def save_sync_state(
    user_id: str,
    email_address: str,
    history_id: str,
):
    """
    Save the latest Gmail history ID for an account.
    """

    doc_ref = (
        db.collection("users")
        .document(user_id)
        .collection("gmail_accounts")
        .document(email_address)
    )

    doc_ref.set(
        {
            "email": email_address,
            "history_id": history_id,
            "last_synced_at": datetime.now(timezone.utc),
        },
        merge=True,
    )