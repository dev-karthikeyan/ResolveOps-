from middleware.pii_middleware import redact_ticket_pii
from middleware.guardrails import run_guardrails, GuardrailViolation


def process_input(state):
    """
    Sanitize and validate the incoming ticket before it enters
    the pipeline. Runs PII redaction and guardrail checks.
    """

    ticket = state["ticket"]

    try:
        run_guardrails(ticket)

    except GuardrailViolation as violation:
        state["status"] = "Blocked by guardrails"
        state["guardrail_error"] = str(violation)
        state["blocked"] = True
        return state

    state["ticket"] = redact_ticket_pii(ticket)
    state["blocked"] = False

    return state