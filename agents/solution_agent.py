from langchain_core.output_parsers import JsonOutputParser

from prompts.solution_prompt import SOLUTION_PROMPT
from tools.litellm_router import invoke_with_fallback_model

def solution_agent(state):
    """
    Generate the final incident resolution based on
    investigation, root cause, and reflection results.
    """
    ticket = state["ticket"] 
    classification = state["classification"]
    retrieved_evidence = state["retrieved_evidence"]
    investigation = state["investigation"] 
    root_cause = state["root_cause"]
    reflection = state["reflection"]

    prompt = SOLUTION_PROMPT.format(
        json_ticket = ticket, 
        classification = classification, 
        retrieved_evidence = retrieved_evidence, 
        investigation = investigation, 
        root_cause = root_cause, 
        reflection = reflection
    )

    response = invoke_with_fallback_model(

        task = "solution", 
        prompt = prompt
    )

    parser = JsonOutputParser()
    solution = parser.parse(response.content)

    state["solution"] = solution 

    return state

