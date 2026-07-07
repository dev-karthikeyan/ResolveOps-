from schemas.solution_schema import SolutionSchema
from tools.litellm_router import get_model


REQUIRED_KEYS = ["root_cause", "solution", "confidence", "jira_comment"]


def solution_schema_validity(run, example) -> dict:
    """
    Checks whether the final solution conforms to SolutionSchema.
    Score: 1.0 if valid, 0.0 if invalid or missing.
    """

    output = run.outputs or {}
    solution = output.get("solution")

    if not solution:
        return {"key": "solution_schema_validity", "score": 0.0, "comment": "No solution produced"}

    try:
        SolutionSchema(**solution)
        return {"key": "solution_schema_validity", "score": 1.0}

    except Exception as error:
        return {
            "key": "solution_schema_validity",
            "score": 0.0,
            "comment": f"Schema validation failed: {error}",
        }


def confidence_threshold(run, example, threshold: float = 0.5) -> dict:
    """
    Flags runs where the model's own confidence in the solution
    is below a minimum acceptable threshold.
    """

    output = run.outputs or {}
    solution = output.get("solution") or {}
    confidence = solution.get("confidence")

    if confidence is None:
        return {"key": "confidence_threshold", "score": 0.0, "comment": "No confidence score found"}

    score = 1.0 if confidence >= threshold else 0.0

    return {
        "key": "confidence_threshold",
        "score": score,
        "comment": f"Confidence: {confidence}",
    }


def pipeline_completed(run, example) -> dict:
    """
    Checks whether the pipeline ran end-to-end without getting
    blocked by guardrails or crashing before producing a solution.
    """

    output = run.outputs or {}

    blocked = output.get("blocked", False)
    solution = output.get("solution")

    if blocked:
        return {"key": "pipeline_completed", "score": 0.0, "comment": "Blocked by guardrails"}

    if not solution:
        return {"key": "pipeline_completed", "score": 0.0, "comment": "No solution produced"}

    return {"key": "pipeline_completed", "score": 1.0}


def root_cause_relevance_llm_judge(run, example) -> dict:
    """
    LLM-as-judge: rates whether the identified root cause is
    plausible given the original ticket description.
    """

    output = run.outputs or {}
    ticket = (example.inputs or {}).get("ticket", {})
    solution = output.get("solution") or {}

    root_cause = solution.get("root_cause", "")
    description = ticket.get("description", "")

    if not root_cause or not description:
        return {"key": "root_cause_relevance", "score": 0.0, "comment": "Missing root cause or ticket description"}

    judge_prompt = f"""
You are evaluating an incident response AI system.

Ticket description:
{description}

Proposed root cause:
{root_cause}

On a scale of 0.0 to 1.0, how plausible and relevant is this root cause
given the ticket description? Respond with ONLY a number between 0.0 and 1.0.
"""

    judge_model = get_model("reflection")

    response = judge_model.invoke(judge_prompt)

    try:
        score = float(response.content.strip())
        score = max(0.0, min(1.0, score))

    except ValueError:
        score = 0.0

    return {"key": "root_cause_relevance", "score": score}


all_evaluators = [
    solution_schema_validity,
    confidence_threshold,
    pipeline_completed,
    root_cause_relevance_llm_judge,
]