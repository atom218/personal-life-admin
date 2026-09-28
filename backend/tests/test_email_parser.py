import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from gmail_client import get_recent_messages, get_message
from email_parser import get_email_body


messages = get_recent_messages(max_results=5)

print(f"\nChecking {len(messages)} emails...\n")

for message in messages:
    full_message = get_message(message["id"])

    body = get_email_body(full_message)

    print(f"Message ID: {message['id']}")
    print(f"Characters sent to AI: {len(body)}")
    print("-" * 60)