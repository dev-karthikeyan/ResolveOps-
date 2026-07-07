BLOCKED_KEYWORDS = [
    "ignore previous instructions",
    "disregard your instructions",
    "system prompt",
    "you are now",
]

MAX_TICKET_LENGTH = 20000


class GuardrailViolation(Exception):
    """Raised when a ticket fails guardrail checks."""
    pass


def check_prompt_injection(text: str) -> None:
    """
    Basic check for prompt-injection style content in ticket text.
    Not exhaustive — a first line of defense, not a complete solution.
    """
    if not text:
        return

    lowered = text.lower()

    for phrase in BLOCKED_KEYWORDS:
        if phrase in lowered:
            raise GuardrailViolation(
                f"Ticket content contains blocked phrase: '{phrase}'"
            )


def check_length(text: str) -> None:
    if text and len(text) > MAX_TICKET_LENGTH:
        raise GuardrailViolation(
            f"Ticket content exceeds max length of {MAX_TICKET_LENGTH} characters"
        )


def run_guardrails(ticket: dict) -> None:
    """
    Run all guardrail checks against a ticket.
    Raises GuardrailViolation if any check fails.
    """
    description = ticket.get("description", "")
    title = ticket.get("title", "")

    combined_text = f"{title} {description}"

    check_length(combined_text)
    check_prompt_injection(combined_text)