from langsmith import Client

client = Client()

DATASET_NAME = "resolveops-incident-tickets"

SAMPLE_TICKETS = [
    {
        "ticket_id": "INC-1001",
        "title": "Payment API returns HTTP 500",
        "description": "Customers are unable to complete payments due to Internal Server Error.",
        "reporter": "John Doe",
        "priority": "High",
        "status": "OPEN",
    },
    {
        "ticket_id": "INC-1002",
        "title": "Login page throws 502 Bad Gateway",
        "description": "Users report intermittent 502 errors when trying to log in since this morning's deploy.",
        "reporter": "Jane Smith",
        "priority": "Critical",
        "status": "OPEN",
    },
    {
        "ticket_id": "INC-1003",
        "title": "Slow database queries on orders table",
        "description": "Order history page is timing out for some users. Query latency spiked after last night's migration.",
        "reporter": "Alex Kim",
        "priority": "Medium",
        "status": "OPEN",
    },
    {
        "ticket_id": "INC-1004",
        "title": "Users unable to reset password",
        "description": "Password reset emails are not being received. No errors in the UI.",
        "reporter": "Priya Rao",
        "priority": "High",
        "status": "OPEN",
    },
]


def build_dataset():
    """
    Create (or reuse) a LangSmith dataset from SAMPLE_TICKETS.
    Each example's input is a ticket; there's no fixed 'expected output'
    since incident resolution is open-ended — evaluators judge quality
    of the output instead of exact match.
    """

    existing = list(client.list_datasets(dataset_name=DATASET_NAME))

    if existing:
        dataset = existing[0]
        print(f"Dataset '{DATASET_NAME}' already exists, reusing it.")
        return dataset

    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description="Sample incident tickets for evaluating ResolveOps end-to-end.",
    )

    for ticket in SAMPLE_TICKETS:
        client.create_example(
            inputs={"ticket": ticket},
            outputs={},
            dataset_id=dataset.id,
        )

    print(f"Created dataset '{DATASET_NAME}' with {len(SAMPLE_TICKETS)} examples.")

    return dataset


if __name__ == "__main__":
    build_dataset()