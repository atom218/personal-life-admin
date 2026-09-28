from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

BASE_DIR = Path(__file__).resolve().parents[1]

SECRETS_DIR = BASE_DIR / "secrets"

CREDENTIALS_FILE = SECRETS_DIR / "credentials.json"
TOKEN_FILE = SECRETS_DIR / "gmail_token.json"


def get_gmail_service():
    credentials = None

    # Reuse an existing login if we already have one.
    if TOKEN_FILE.exists():
        credentials = Credentials.from_authorized_user_file(
            str(TOKEN_FILE),
            SCOPES,
        )

    # Refresh an expired token if possible.
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    # Otherwise, start the Google login flow.
    if not credentials or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(CREDENTIALS_FILE),
            SCOPES,
        )

        credentials = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(credentials.to_json())

    return build("gmail", "v1", credentials=credentials)


def get_recent_messages(max_results=5):
    service = get_gmail_service()

    response = (
        service.users()
        .messages()
        .list(
            userId="me",
            maxResults=max_results,
        )
        .execute()
    )

    return response.get("messages", [])


def get_message(message_id):
    service = get_gmail_service()

    return (
        service.users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format="full",
        )
        .execute()
    )


def get_profile():
    """
    Get the authenticated Gmail account's profile information.
    """

    service = get_gmail_service()

    return (
        service.users()
        .getProfile(
            userId="me",
        )
        .execute()
    )


def get_history(start_history_id):
    """
    Get Gmail mailbox changes that occurred after start_history_id.
    """

    service = get_gmail_service()

    response = (
        service.users()
        .history()
        .list(
            userId="me",
            startHistoryId=start_history_id,
            historyTypes=["messageAdded"],
        )
        .execute()
    )

    return response