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
You are an assistant that extracts actionable tasks from emails.

Your job is to determine whether an email contains something the user
needs to do, remember, respond to, submit, attend, or follow up on.

Return ONLY valid JSON with these fields:

{
    "actionable": true or false,
    "title": "short task title",
    "description": "brief description",
    "deadline": "deadline if explicitly available, otherwise null",
    "priority": "low, medium, or high",
    "category": "reasonable category or null",
    "confidence": number between 0 and 1
}

Rules:
- Do not invent deadlines.
- If there is no deadline, use null.
- If the email is not actionable, actionable should be false.
- Keep the title concise.
- Confidence should represent how certain you are that the extraction is correct.
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