from tools.slack_tool import send_slack_notification


def slack_notification_agent(state):
    """
    Send a Slack notification after the Jira ticket
    has been successfully updated.
    """

    jira_update = state.get("jira_update")

    if not jira_update or not jira_update.get("success", False):
        state["status"] = "Slack Notification Skipped"
        return state

    ticket = state["ticket"]
    solution = state["solution"]

    message = f"""
🚨 Incident Resolved

Ticket ID: {ticket["ticket_id"]}
Title: {ticket["title"]}

Root Cause:
{solution["root_cause"]}

Recommended Solution:
{solution["solution"]}

Confidence:
{solution["confidence"]:.2f}

Jira Status:
Updated Successfully ✅
"""

    result = send_slack_notification(message)

    state["slack_notification"] = result
    state["status"] = "Slack Notification Sent"

    return state