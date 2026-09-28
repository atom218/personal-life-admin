import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from task_service import get_tasks


USER_ID = "test-user"


def test_get_tasks():
    tasks = get_tasks(USER_ID)

    print("\n")
    print("=" * 60)
    print("TASKS")
    print("=" * 60)

    print(f"Number of tasks: {len(tasks)}")

    for task in tasks:
        print("\nTask:")
        print(task)

    assert isinstance(tasks, list)