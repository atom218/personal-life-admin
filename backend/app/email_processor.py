from firebase import db
from gmail_client import get_message
from email_parser import get_email_body
from email_tracker import is_email_processed, mark_email_processed
from email_filter import should_skip_email
from groq_client import extract_task


def save_task(user_id: str, task, message_id: str):
    task_data = task.model_dump()

    task_data["source"] = {
        "type": "gmail",
        "message_id": message_id,
    }

    (
        db.collection("users")
        .document(user_id)
        .collection("tasks")
        .add(task_data)
    )


def process_email(user_id: str, message_id: str):
    """
    Process one Gmail message from start to finish.

    Returns a status string describing what happened.
    """

    # --------------------------------------------------
    # 1. Check whether we've already processed it
    # --------------------------------------------------

    if is_email_processed(user_id, message_id):
        return "already_processed"

    # --------------------------------------------------
    # 2. Fetch the Gmail message
    # --------------------------------------------------

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

    # --------------------------------------------------
    # 3. Extract readable email body
    # --------------------------------------------------

    body = get_email_body(message)

    if not body:
        mark_email_processed(user_id, message_id)
        return "empty"

    # --------------------------------------------------
    # 4. Lightweight noise filter
    # --------------------------------------------------

    if should_skip_email(subject, body):
        mark_email_processed(user_id, message_id)
        return "filtered"

    # --------------------------------------------------
    # 5. AI classification
    # --------------------------------------------------

    task = extract_task(
        subject=subject,
        sender=sender,
        body=body,
    )

    # --------------------------------------------------
    # 6. Create task only when actionable
    # --------------------------------------------------

    if task.actionable:
        save_task(
            user_id=user_id,
            task=task,
            message_id=message_id,
        )

        mark_email_processed(user_id, message_id)

        return "task_created"

    # --------------------------------------------------
    # 7. Email processed but no task needed
    # --------------------------------------------------

    mark_email_processed(user_id, message_id)

    return "no_task"