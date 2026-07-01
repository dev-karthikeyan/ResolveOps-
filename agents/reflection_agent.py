from langchain_core.output_parsers import JsonOutputParser

from prompts.reflection_prompt import REFLECTION_PROMPT
from tools.litellm_router import invoke_with_fallback_model

def reflection_agent(state) :
      """
    Review the root cause analysis and solution reasoning.
    Identify inconsistencies, missing evidence, or low confidence.
    """
      ticket = state["ticket"] 
      classification = state["classification"]
      retrieved_evidence = state["retrieved_evidence"]
      investigation = state["investigation"] 
      root_cause = state["root_cause"]

      prompt = REFLECTION_PROMPT.format(
        json_ticket = ticket ,
        classification = classification ,
        retrieved_evidence = retrieved_evidence ,
        investigation = investigation ,
        root_cause = root_cause 
)
    
      response = invoke_with_fallback_model(
            
            task = "reflection" ,
            prompt = prompt
)      

      parser = JsonOutputParser()

      reflection = parser.parse(response.content)

      state["reflection"] = reflection 

      return state
