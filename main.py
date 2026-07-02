from graphs.workflow import graph


def main():

    ticket = {
        "ticket_id": "INC-1001",
        "title": "Payment API returns HTTP 500",
        "description": "Customers are unable to complete payments due to Internal Server Error.",
        "reporter": "John Doe",
        "priority": "High",
        "status": "OPEN",
    }

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
    }

    result = graph.invoke(initial_state)

    print("\n========== FINAL RESULT ==========\n")
    print(result)


if __name__ == "__main__":
    main()