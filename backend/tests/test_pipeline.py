import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from gmail_client import get_recent_messages, get_message
from email_parser import get_email_body
from email_tracker import is_email_processed, mark_email_processed
from email_filter import should_skip_email
from groq_client import extract_task
from firebase import db


USER_ID = "test-user"


def save_task(task, message_id):
    task_data = task.model_dump()

    task_data["source"] = {
        "type": "gmail",
        "message_id": message_id,
    }

    db.collection("users") \
        .document(USER_ID) \
        .collection("tasks") \
        .add(task_data)


def process_email(message_id):
    if is_email_processed(USER_ID, message_id):
        print(f"SKIP PROCESSED: {message_id}")
        return

    message = get_message(message_id)

    headers = message.get("payload", {}).get("headers", [])

    subject = ""
    sender = ""

    for header in headers:
        name = header.get("name", "").lower()

        if name == "subject":
            subject = header.get("value", "")

        elif name == "from":
            sender = header.get("value", "")

    body = get_email_body(message)

    if not body:
        print(f"SKIP EMPTY: {message_id}")
        mark_email_processed(USER_ID, message_id)
        return

    # --------------------------------------------------
    # STEP 1: Lightweight noise filter
    # --------------------------------------------------

    if should_skip_email(subject, body):
        print(f"SKIP FILTER: {subject}")
        mark_email_processed(USER_ID, message_id)
        return

    # --------------------------------------------------
    # STEP 2: AI classification
    # --------------------------------------------------

    print(f"AI PROCESSING: {subject}")

    try:
        task = extract_task(
            subject=subject,
            sender=sender,
            body=body,
        )

        print(f"Actionable: {task.actionable}")
        print(f"Reason: {task.reason}")

        if task.actionable:
            save_task(task, message_id)
            print(f"TASK CREATED: {task.title}")
        else:
            print("NO TASK CREATED")

        mark_email_processed(USER_ID, message_id)

    except Exception as e:
        print(f"ERROR PROCESSING {message_id}: {e}")


def main():
    messages = get_recent_messages(max_results=30)

    print(f"Found {len(messages)} recent emails.")
    print("=" * 70)

    for message in messages:
        process_email(message["id"])
        print("-" * 70)


if __name__ == "__main__":
    main()