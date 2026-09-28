import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from firebase import db


USER_ID = "test-user"


def test_list_tasks():
    tasks_ref = (
        db.collection("users")
        .document(USER_ID)
        .collection("tasks")
    )

    documents = tasks_ref.stream()

    tasks = list(documents)

    print("\n")
    print("=" * 60)
    print("TASKS IN FIRESTORE")
    print("=" * 60)

    print(f"Number of tasks: {len(tasks)}")

    for document in tasks:
        print(f"\nDocument ID: {document.id}")
        print(document.to_dict())

    assert len(tasks) >= 1