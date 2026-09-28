from gmail_client import get_profile, get_history, get_message
from email_processor import process_email
from gmail_sync_state import get_sync_state, save_sync_state


def sync_gmail(user_id: str):
    """
    Incrementally sync one Gmail account.

    First sync:
        Establishes a starting history ID.

    Later syncs:
        Processes messages added since the previous history ID.
    """

    profile = get_profile()

    email_address = profile["emailAddress"]
    current_history_id = profile["historyId"]

    print(f"Gmail account: {email_address}")
    print(f"Current history ID: {current_history_id}")

    state = get_sync_state(
        user_id=user_id,
        email_address=email_address,
    )

    # --------------------------------------------------
    # First sync
    # --------------------------------------------------

    if state is None:
        save_sync_state(
            user_id=user_id,
            email_address=email_address,
            history_id=current_history_id,
        )

        print("First sync completed.")
        print("Starting history ID saved.")

        return {
            "email": email_address,
            "first_sync": True,
            "messages_found": 0,
            "tasks_created": 0,
        }

    # --------------------------------------------------
    # Incremental sync
    # --------------------------------------------------

    previous_history_id = state["history_id"]

    print(f"Previous history ID: {previous_history_id}")

    history_response = get_history(previous_history_id)

    message_ids = set()

    for history_item in history_response.get("history", []):
        for message in history_item.get("messagesAdded", []):
            message_ids.add(message["message"]["id"])

    print(f"New messages found: {len(message_ids)}")

    tasks_created = 0

    for message_id in message_ids:
        try:
            result = process_email(
                user_id=user_id,
                message_id=message_id,
            )

            print(f"{message_id}: {result}")

            if result == "task_created":
                tasks_created += 1

        except Exception as e:
            print(f"Error processing {message_id}: {e}")

    # --------------------------------------------------
    # Save the new history ID
    # --------------------------------------------------

    save_sync_state(
        user_id=user_id,
        email_address=email_address,
        history_id=current_history_id,
    )

    print(f"Sync state updated to: {current_history_id}")

    return {
        "email": email_address,
        "first_sync": False,
        "messages_found": len(message_ids),
        "tasks_created": tasks_created,
    }