from langsmith.evaluation import evaluate

from evaluation.dataset import build_dataset, DATASET_NAME
from evaluation.evaluators import all_evaluators
from graphs.workflow import graph


def target(inputs: dict) -> dict:
    """
    Wraps the compiled LangGraph graph so LangSmith can invoke it
    per dataset example.
    """

    ticket = inputs["ticket"]

    initial_state = {
        "ticket": ticket,
        "classification": None,
        "retrieved_evidence": None,
        "investigation": None,
        "root_cause": None,
        "reflection": None,
        "solution": None,
        "approved": True,
        "status": None,
        "blocked": False,
    }

    result = graph.invoke(initial_state)

    return result


def run_evaluation():
    build_dataset()

    results = evaluate(
        target,
        data=DATASET_NAME,
        evaluators=all_evaluators,
        experiment_prefix="resolveops-eval",
        max_concurrency=2,
    )

    print("\n========== EVALUATION COMPLETE ==========\n")
    print(results)

    return results


if __name__ == "__main__":
    run_evaluation()