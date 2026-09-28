import re


IGNORE_PATTERNS = [
    # Job alerts / newsletters
    r"unsubscribe",
    r"weekly newsletter",
    r"job alert",
    r"new jobs",
    r"recommended jobs",

    # Delivery / shipping notifications
    r"order has shipped",
    r"order has been delivered",
    r"package was delivered",
    r"package has been delivered",
    r"delivery notification",
    r"left at your (front )?door",

    # Marketing / promotions
    r"special offer",
    r"limited time offer",
    r"sale ends",
    r"promotional",
]


def should_skip_email(subject: str, body: str) -> bool:
    """
    Returns True when an email is very likely to be
    informational, promotional, or an automated notification
    that does not require personal action.
    """

    text = f"{subject}\n{body}".lower()

    for pattern in IGNORE_PATTERNS:
        if re.search(pattern, text):
            return True

    return False