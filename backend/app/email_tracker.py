from firebase import db


def is_email_processed(user_id, message_id):
    doc_ref = (
        db.collection("users")
        .document(user_id)
        .collection("processed_emails")
        .document(message_id)
    )

    return doc_ref.get().exists


def mark_email_processed(user_id, message_id):
    doc_ref = (
        db.collection("users")
        .document(user_id)
        .collection("processed_emails")
        .document(message_id)
    )

    doc_ref.set({
        "message_id": message_id,
        "status": "processed",
    })