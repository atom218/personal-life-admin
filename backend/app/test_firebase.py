from firebase import db


test_task = {
    "title": "Test Firebase connection",
    "description": "This is a test task created from Python.",
    "status": "pending",
    "priority": "medium",
}


doc_ref = (
    db.collection("users")
    .document("test-user")
    .collection("tasks")
    .document("test-task")
)

doc_ref.set(test_task)

print("Successfully created test task!")
print(f"Document ID: {doc_ref.id}")