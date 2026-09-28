from groq_client import extract_task
from firebase import db


sample_email = """
Hi Vandan,

Please submit the first draft of your independent study report
by Friday at 5 PM.

Make sure the experiment results are included.

Thanks,
Professor
"""


task = extract_task(sample_email)

print("\nAI extracted:")
print(task.model_dump_json(indent=2))


if task.actionable:

    task_data = task.model_dump()

    task_data["source"] = {
        "type": "test_email",
        "content": sample_email,
    }

    doc_ref = (
        db.collection("users")
        .document("test-user")
        .collection("tasks")
        .add(task_data)
    )

    print("\nTask successfully saved to Firebase!")
    print(f"Document reference: {doc_ref[1].id}")

else:
    print("\nNo actionable task detected.")