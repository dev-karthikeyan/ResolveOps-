from tools.jira_tool import update_jira_ticket

def jira_update_agent(state) :
    """
    Update the Jira ticket with the generated solution
    after human approval.
    """

    if not state.get("approved" , False) :
        state["status"] = "awaiting dor human approval"
        return state

    ticket = state["ticket"]
    solution = state["solution"]

    result = update_jira_ticket(
        ticket_id=ticket["ticket_id"],
        comment=solution["jira_comment"],
    )

    print("JIRA RESULT:", result)

    state["jira_update"] = result
    state["status"] = "Jira Updated"

    return state