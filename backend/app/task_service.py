from datetime import datetime, timezone

from firebase import db


def get_tasks(user_id: str):
    """
    Retrieve all tasks for a user from Firestore.
    """

    tasks_ref = (
        db.collection("users")
        .document(user_id)
        .collection("tasks")
    )

    documents = tasks_ref.stream()

    tasks = []

    for document in documents:
        task = document.to_dict()

        task["id"] = document.id

        # Older tasks may not have a status.
        # Treat them as pending.
        if "status" not in task:
            task["status"] = "pending"

        tasks.append(task)

    return tasks


def complete_task(user_id: str, task_id: str):
    """
    Mark a task as completed.
    """

    task_ref = (
        db.collection("users")
        .document(user_id)
        .collection("tasks")
        .document(task_id)
    )

    document = task_ref.get()

    if not document.exists:
        return None

    task_ref.update(
        {
            "status": "completed",
            "completed_at": datetime.now(timezone.utc),
        }
    )

    return True