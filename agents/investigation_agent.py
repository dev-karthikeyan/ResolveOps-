from langchain_core.output_parsers import JsonOutputParser

from prompts.investigation_prompt import INVESTIGATION_PROMPT
from tools.litellm_router import invoke_with_fallback_model

def investigation_agent (state) :
    """
    Build incident timeline and investigation summary.
    """

    ticket = state["ticket"]
    classification = state["classification"]
    retrieved_evidence = state["retrieved_evidence"]

    prompt = INVESTIGATION_PROMPT.format(

         ticket_json = ticket ,
         classification = classification ,
         retrieved_evidence = retrieved_evidence
)

    response = invoke_with_fallback_model(
        
        task = "investigation" ,
        prompt = prompt
)
    parser = JsonOutputParser()
    
    investigation = parser.parse(response.content)

    state["investigation"] = investigation

    return state 

    