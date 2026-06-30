from langsmith.schemas import Prompt
from langchain_core.output_parsers import JsonOutputParser

from prompts.retrieval_prompt import RETRIEVAL_PROMPT
from tools.litellm_router import invoke_with_fallback_model

def rag_retrieval_agent(state) :
    """
    Retrieve relevant evidence based on ticket classification.
    """
    
    classification = state["classification"]
    ticket = state["ticket"]  

    Prompt = RETRIEVAL_PROMPT.format(
         classification = state["classification"] ,
         ticket_json = ticket 
)

    response = invoke_with_fallback_model(
      
         task = "retrieval" ,
         prompt= Prompt
)

    parser = JsonOutputParser()

    retrieved_evidence  = parser.parse(response.content)

    state["retrieved_evidence"] = retrieved_evidence 

    return state 