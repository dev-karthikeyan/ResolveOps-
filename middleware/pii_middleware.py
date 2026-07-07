import re


PII_PATTERNS = {
    "email": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    "phone": re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"),
    "ip_address": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "credit_card": re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
}


def redact_pii(text: str) -> str:
    """
    Redact common PII patterns from a string.
    IP addresses are kept since they're often operationally relevant
    for incident response — remove that line if you want them redacted too.
    """
    if not text:
        return text

    redacted = text

    for label, pattern in PII_PATTERNS.items():
        if label == "ip_address":
            continue
        redacted = pattern.sub(f"[REDACTED_{label.upper()}]", redacted)

    return redacted


def redact_ticket_pii(ticket: dict) -> dict:
    """
    Redact PII from all string fields in a ticket dict.
    """
    redacted_ticket = dict(ticket)

    for key, value in redacted_ticket.items():
        if isinstance(value, str):
            redacted_ticket[key] = redact_pii(value)

    return redacted_ticket