from langchain_core.output_parsers import JsonOutputParser

from prompts.rootcause_prompt import ROOTCAUSE_PROMPT
from tools.litellm_router import invoke_with_fallback_model

def root_cause_agent(state) :
    """
    Analyze the investigation results and determine
    the most likely root cause of the incident.
    """

    ticket = state["ticket"] 
    classification = state["classification"]
    retrieved_evidence = state["retrieved_evidence"]
    investigation = state["investigation"] 

    prompt = ROOTCAUSE_PROMPT.format(

        json_ticket = ticket ,
        classification = classification ,
        retrieved_evidence = retrieved_evidence ,
        investigation = investigation 
)   
    
    response = invoke_with_fallback_model(
   
        task = "root_cause" ,
        prompt= prompt
)

    parser = JsonOutputParser()

    root_cause = parser.parse(response.content)
    
    state["root_cause"] = root_cause

    return state 