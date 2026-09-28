from gmail_client import get_recent_messages, get_message
from email_parser import get_email_body
from groq_client import extract_task
from email_tracker import is_email_processed, mark_email_processed
from firebase import db


USER_ID = "test-user"


messages = get_recent_messages(max_results=5)

print(f"\nProcessing {len(messages)} emails...\n")


for message in messages:

    message_id = message["id"]

    # Prevent duplicate processing
    if is_email_processed(USER_ID, message_id):
        print(f"Skipping {message_id} - already processed.")
        print("-" * 60)
        continue

    full_message = get_message(message_id)

    body = get_email_body(full_message)

    if not body:
        print(f"Skipping {message_id} - no readable text body.")

        # We still mark it as processed so we don't repeatedly
        # attempt the same unsupported email.
        mark_email_processed(USER_ID, message_id)

        print("-" * 60)
        continue

    print(f"Processing {message_id}...")
    print(f"Characters sent to AI: {len(body)}")

    try:
        task = extract_task(body)

        print("\nAI extracted:")
        print(task.model_dump_json(indent=2))

        if task.actionable:

            task_data = task.model_dump()

            task_data["source"] = {
                "type": "gmail",
                "message_id": message_id,
            }

            doc_ref = (
                db.collection("users")
                .document(USER_ID)
                .collection("tasks")
                .add(task_data)
            )

            print(f"\nTask saved to Firebase: {doc_ref[1].id}")

        else:
            print("\nNo actionable task detected.")

        # Only mark as processed after successful AI processing
        mark_email_processed(USER_ID, message_id)

    except Exception as error:
        print(f"\nFailed to process email: {error}")

    print("-" * 60)