import base64
import re

from bs4 import BeautifulSoup


MAX_EMAIL_CHARS = 8000


def get_email_body(message):
    payload = message.get("payload", {})

    body = extract_text_from_payload(payload)

    if not body:
        return ""

    # Clean excessive whitespace
    body = re.sub(r"\n\s*\n\s*\n+", "\n\n", body)
    body = re.sub(r"[ \t]+", " ", body)

    # Limit the amount sent to the AI
    if len(body) > MAX_EMAIL_CHARS:
        body = body[:MAX_EMAIL_CHARS]

    return body.strip()


def extract_text_from_payload(payload):
    mime_type = payload.get("mimeType", "")

    # Plain text email
    if mime_type == "text/plain":
        data = payload.get("body", {}).get("data")

        if data:
            return decode_body(data)

    # HTML email
    if mime_type == "text/html":
        data = payload.get("body", {}).get("data")

        if data:
            html = decode_body(data)
            return html_to_text(html)

    # Multipart email
    for part in payload.get("parts", []):
        result = extract_text_from_payload(part)

        if result:
            return result

    return ""


def decode_body(data):
    return base64.urlsafe_b64decode(data).decode(
        "utf-8",
        errors="replace",
    )


def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove elements that don't contain useful email content
    for element in soup(["script", "style", "noscript"]):
        element.decompose()

    return soup.get_text(separator="\n")