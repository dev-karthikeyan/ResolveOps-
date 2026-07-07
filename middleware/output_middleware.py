from middleware.pii_middleware import redact_pii


REQUIRED_SOLUTION_KEYS = ["root_cause", "solution", "confidence", "jira_comment"]


class OutputValidationError(Exception):
    pass


def validate_solution(solution: dict) -> None:
    missing = [key for key in REQUIRED_SOLUTION_KEYS if key not in solution]

    if missing:
        raise OutputValidationError(
            f"Solution output missing required keys: {missing}"
        )


def process_output(state):
    """
    Validate and sanitize the generated solution before it gets
    posted to Jira/Slack.
    """

    solution = state["solution"]

    try:
        validate_solution(solution)

    except OutputValidationError as error:
        state["status"] = "Blocked: invalid solution output"
        state["output_error"] = str(error)
        state["blocked"] = True
        return state

    solution["jira_comment"] = redact_pii(solution["jira_comment"])
    solution["solution"] = redact_pii(solution["solution"])

    state["solution"] = solution

    return state