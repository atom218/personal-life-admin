import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from firebase import db


USER_ID = "test-user"

TASK_IDS_TO_DELETE = [
    "FSlzbx1jrskyfdgzXswB",
    "MlyrdnDGRDuzLlxuAhQU",
    "QkUMKEyohFVVJVH6hXtG",
    "SNZrqvtu76uUU00lKbTo",
    "Y7OSzkzRBskV64oIaKM7",
    "k09sbsMZeiRDO4Grdlh3",
    "kpnh0CsYrPUP30tpwCKt",
    "oCduFU91enQD1f8KMWTa",
    "tjERf7KiXmA8vruhCcnG",
    "test-task",
]


def delete_tasks():
    tasks_ref = (
        db.collection("users")
        .document(USER_ID)
        .collection("tasks")
    )

    for task_id in TASK_IDS_TO_DELETE:
        document_ref = tasks_ref.document(task_id)

        if document_ref.get().exists:
            document_ref.delete()
            print(f"Deleted: {task_id}")
        else:
            print(f"Not found: {task_id}")


if __name__ == "__main__":
    delete_tasks()