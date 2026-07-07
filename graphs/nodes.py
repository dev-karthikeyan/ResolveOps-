
from agents.ticket_classifier_agent import ticket_classifier_agent
from agents.rag_retrieval_agent import rag_retrieval_agent
from agents.investigation_agent import investigation_agent
from agents.root_cause_agent import root_cause_agent
from agents.reflection_agent import reflection_agent
from agents.solution_agent import solution_agent
from agents.jira_update_agent import jira_update_agent
from agents.slack_notification_agent import slack_notification_agent
from middleware.input_middleware import process_input
from middleware.output_middleware import process_output

input_middleware_node = process_input
output_middleware_node = process_output

classifier_node = ticket_classifier_agent

retriever_node = rag_retrieval_agent

investigation_node = investigation_agent

root_cause_node = root_cause_agent 

reflection_node = reflection_agent

solution_node = solution_agent

jira_update_node = jira_update_agent

slack_notification_node = slack_notification_agent 


