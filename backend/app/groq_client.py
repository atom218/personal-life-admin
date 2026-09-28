import os
import json

from dotenv import load_dotenv
from groq import Groq

from models import ExtractedTask


from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(ENV_PATH)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set in the .env file.")

client = Groq(api_key=api_key)


SYSTEM_PROMPT = """
You are an intelligent personal life-admin assistant.

Your job is to analyze an email and determine whether the USER personally
needs to take an action because of the email.

Return ONLY valid JSON with these fields:

{
    "actionable": true or false,
    "title": "short task title",
    "description": "brief description",
    "deadline": "explicit deadline if available, otherwise null",
    "priority": "low, medium, or high",
    "category": "reasonable category or null",
    "confidence": number between 0 and 1,
    "reason": "brief explanation of why the email is or is not actionable"
}

IMPORTANT DEFINITION:

An email is ACTIONABLE only when the user personally needs to do
something, remember something, respond to someone, attend something,
submit something, decide something, or follow up on something.

An email is NOT actionable merely because it contains information that
the user may find useful.

Examples of NOT actionable emails:

- Job alerts listing multiple jobs without asking the user to apply.
- Newsletters.
- Marketing emails.
- Promotional offers.
- General announcements that require no response.
- Delivery notifications when no action is required.
- Receipts or confirmations that require no action.
- Informational emails.

Examples of ACTIONABLE emails:

- "Please submit the report by Friday."
- "Can you send me the revised document?"
- "Your assignment is due tomorrow."
- "Please RSVP for the event."
- "You need to complete this form."
- "Please review this document and send your feedback."
- "Registration closes Friday and you need to register."

IMPORTANT RULES:

1. Do not invent deadlines.
2. If there is no explicit deadline, use null.
3. Do not interpret general usefulness as an action.
4. If an email contains optional information, it should normally be
   non-actionable.
5. A task should represent something the user personally needs to do.
6. Keep the title concise and action-oriented.
7. Priority should reflect urgency and importance:
   - high: important or time-sensitive
   - medium: meaningful action without immediate urgency
   - low: minor or non-urgent action
8. Confidence must be between 0 and 1.
9. When uncertain, prefer actionable=false and lower confidence.
10. Return ONLY JSON. Do not include markdown or additional text.
"""


def extract_task(email_text: str) -> ExtractedTask:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": email_text,
            },
        ],
    )

    content = response.choices[0].message.content

    data = json.loads(content)

    return ExtractedTask(**data)