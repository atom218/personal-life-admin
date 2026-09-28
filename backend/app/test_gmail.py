from gmail_client import get_recent_messages, get_message


messages = get_recent_messages(max_results=5)

print(f"\nFound {len(messages)} recent messages.\n")

for message in messages:
    full_message = get_message(message["id"])

    headers = full_message["payload"].get("headers", [])

    subject = ""
    sender = ""

    for header in headers:
        if header["name"].lower() == "subject":
            subject = header["value"]

        if header["name"].lower() == "from":
            sender = header["value"]

    print(f"From: {sender}")
    print(f"Subject: {subject}")
    print(f"Message ID: {message['id']}")
    print("-" * 60)