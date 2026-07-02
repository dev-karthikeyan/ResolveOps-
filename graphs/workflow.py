from langgraph.graph import StateGraph, START, END

from schemas.state_schema import ResolveOpsState
from graphs.nodes import (
    classifier_node,
    retriever_node,
    investigation_node,
    root_cause_node,
    reflection_node,
    solution_node,
    jira_update_node,
    slack_notification_node,
)


builder = StateGraph(ResolveOpsState)


builder.add_node("classifier", classifier_node)
builder.add_node("retriever", retriever_node)
builder.add_node("investigation", investigation_node)
builder.add_node("root_cause", root_cause_node)
builder.add_node("reflection", reflection_node)
builder.add_node("solution", solution_node)
builder.add_node("jira_update", jira_update_node)
builder.add_node("slack_notification", slack_notification_node)



builder.add_edge(START, "classifier")

builder.add_edge("classifier", "retriever")
builder.add_edge("retriever", "investigation")
builder.add_edge("investigation", "root_cause")
builder.add_edge("root_cause", "reflection")
builder.add_edge("reflection", "solution")
builder.add_edge("solution", "jira_update")
builder.add_edge("jira_update", "slack_notification")


builder.add_edge("slack_notification", END)


graph = builder.compile()